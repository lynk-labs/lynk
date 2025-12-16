import React, { createContext, useEffect, useState, useCallback, ReactNode, useRef } from 'react';
import { useWallet, WalletProvider } from '@solana/wallet-adapter-react';
import { Adapter } from '@solana/wallet-adapter-base';
import { LynkContextState, LynkConfig } from './types';
import { SessionManager } from './utils/storage';
import { attemptHealing } from './utils/reconnect';

export const LynkContext = createContext<LynkContextState>({} as LynkContextState);

interface LynkProviderProps extends LynkConfig {
    children: ReactNode;
    wallets: Adapter[];
    onError?: (error: Error) => void;
}

// Fixed: Explicit type annotation for props to satisfy TS strict mode
export const LynkProvider = ({ 
    children, 
    wallets, 
    autoConnect = true,
    storagePrefix,
    onError
}: LynkProviderProps) => {
    // We pass autoConnect=false to the inner WalletProvider because LYNK handles it manually
    // to provide the "Healing" capabilities.
    return (
        <WalletProvider wallets={wallets} autoConnect={false}>
            <LynkInner 
                config={{ autoConnect, storagePrefix, onError }} 
                wallets={wallets}
            >
                {children}
            </LynkInner>
        </WalletProvider>
    );
};

interface InnerProps {
    children: ReactNode;
    config: LynkConfig;
    wallets: Adapter[];
}

// Fixed: Explicit type annotation for InnerProps
const LynkInner = ({ children, config, wallets }: InnerProps) => {
    const { 
        connected, 
        connecting, 
        disconnecting, 
        wallet, 
        connect, 
        disconnect: baseDisconnect, 
        publicKey,
        select 
    } = useWallet();

    const [isHealing, setIsHealing] = useState(false);
    const sessionManager = useRef(new SessionManager(config.storagePrefix));
    const mounted = useRef(false);

    // 1. Mount & Initial Auto-Connect Logic
    useEffect(() => {
        mounted.current = true;
        
        const initSession = async () => {
            if (connected || connecting) return;

            const session = sessionManager.current.getSession();
            if (session && config.autoConnect) {
                console.log(`[LYNK] Found session for ${session.walletName}. Initiating healing...`);
                
                // Select the wallet first
                select(session.walletName as any);
                
                // Trigger healing
                handleHealing();
            }
        };

        initSession();

        return () => { mounted.current = false; };
    }, []);

    // 2. Session Persistence Observer
    useEffect(() => {
        if (connected && publicKey && wallet) {
            sessionManager.current.setSession(wallet.adapter.name, publicKey.toBase58());
        }
    }, [connected, publicKey, wallet]);

    // 3. The "Healing" Function
    const handleHealing = useCallback(async () => {
        if (isHealing) return;
        
        setIsHealing(true);
        
        try {
            const success = await attemptHealing(
                async () => {
                    await connect();
                },
                () => connected, // Check function
                { maxAttempts: 4, initialDelay: 200 }
            );

            if (!success) {
                throw new Error("Healing sequence exhausted.");
            }
        } catch (e) {
            console.error("[LYNK] Healing failed:", e);
            // Clear session if we truly can't reconnect
            sessionManager.current.clearSession();
            if (config.onError) config.onError(e as Error);
        } finally {
            if (mounted.current) setIsHealing(false);
        }
    }, [connect, connected, config, isHealing]);

    // 4. Custom Disconnect (Clears Session)
    const handleDisconnect = useCallback(async () => {
        sessionManager.current.clearSession();
        await baseDisconnect();
    }, [baseDisconnect]);

    const contextValue: LynkContextState = {
        connected,
        connecting: connecting || isHealing,
        disconnecting,
        heal: handleHealing,
        disconnect: handleDisconnect,
        publicKey: publicKey || null,
        sessionSignature: sessionManager.current.getSession()?.publicKey || null
    };

    return (
        <LynkContext.Provider value={contextValue}>
            {children}
        </LynkContext.Provider>
    );
};
