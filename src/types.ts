import { WalletAdapterNetwork, Adapter } from '@solana/wallet-adapter-base';
import { PublicKey } from '@solana/web3.js';

export type ReconnectStrategy = 'lazy' | 'aggressive' | 'standard';

export interface AutoConnectConfig {
    /**
     * How aggressively to attempt reconnection on load.
     * - lazy: Only check storage, no active probing.
     * - standard: Check storage and basic wallet readiness.
     * - aggressive: Active polling for wallet injection.
     */
    strategy: ReconnectStrategy;
    
    /**
     * Timeout in milliseconds before giving up on auto-connect.
     * @default 10000
     */
    timeout?: number;
}

export interface LynkConfig {
    /**
     * Configuration for the auto-connection and healing mechanism.
     */
    autoConnect?: boolean | AutoConnectConfig;
    
    /**
     * Optional key prefix for local storage to avoid collisions.
     * @default 'lynk_v1_'
     */
    storagePrefix?: string;
    
    /**
     * Callback when a healing attempt fails definitively.
     */
    onError?: (error: Error) => void;
}

export interface LynkContextState {
    /** Whether the wallet is currently connected */
    connected: boolean;
    
    /** Whether a connection or healing attempt is in progress */
    connecting: boolean;
    
    /** Whether the wallet is disconnecting */
    disconnecting: boolean;
    
    /** The connected wallet's public key */
    publicKey: PublicKey | null;
    
    /** * Manually trigger the healing process. 
     * Useful if the user wants to retry a failed auto-connect.
     */
    heal: () => Promise<void>;
    
    /** Disconnect and clear the session */
    disconnect: () => Promise<void>;
    
    /** The current session signature (if any) */
    sessionSignature: string | null;
}
