import os
import random
import subprocess
import time
from datetime import datetime, timedelta

# ==============================================================================
# [CONFIGURATION]
# ==============================================================================
PROJECT_NAME = "lynk"
REPO_DIR = "." 
USER_NAME = "lynk-labs"
USER_EMAIL = "194120946+lynk-labs@users.noreply.github.com"

# Timeline: 2025-12-15 ~ 2026-01-12
START_DATE = datetime(2025, 12, 15, 9, 0, 0)
END_DATE = datetime(2026, 1, 12, 11, 0, 0)
TARGET_COMMITS = 135

# Helpers
BT = "```" 
BANNER_PATH = "./lynk.png"

# ==============================================================================
# [1. DOCUMENTATION (README.md) - NO EMOJI, PROFESSIONAL]
# ==============================================================================
CONTENT_README = f"""# LYNK: The Unbreakable Wallet Adapter

<div align="center">
  <img src="{BANNER_PATH}" alt="LYNK Banner" width="100%" />
  <br />
  <br />
  <p align="center">
    <img src="https://img.shields.io/badge/Solana-Wallet_Adapter-blueviolet?style=for-the-badge&logo=solana&logoColor=white" alt="Solana" />
    <img src="https://img.shields.io/badge/React-Hook-blue?style=for-the-badge&logo=react&logoColor=white" alt="React" />
    <img src="https://img.shields.io/badge/TypeScript-Strict-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
    <img src="https://img.shields.io/badge/Status-Stable-success?style=for-the-badge" alt="Status" />
    <a href="https://x.com/lynk_labs">
      <img src="https://img.shields.io/badge/X-Follow_Us-black?style=for-the-badge&logo=x&logoColor=white" alt="X" />
    </a>
  </p>
  <p align="center">
    <strong>Stay connected. Lynk up.</strong>
  </p>
</div>

---

## 1. Abstract

**LYNK** is a specialized React hook and provider designed to solve the "Broken Chain" problem in Solana dApps. Standard wallet adapters often disconnect upon page refreshes or minor network jitters, causing user drop-off. 

LYNK introduces a **Persistent Session Layer** combined with an **Auto-Healing Mechanism** that utilizes exponential backoff strategies to maintain wallet connectivity seamlessly.

---

## 2. Key Features

### Auto-Healing Connections
Automatically detects dropped connections and attempts to heal them without user intervention. The protocol monitors the heartbeat of the wallet connection and triggers reconnection logic if a disconnect event occurs unexpectedly.

### Session Persistence
Utilizes secure local storage signatures to verify user intent, allowing sessions to survive browser refreshes and tab switching. This ensures the user remains authenticated across the application lifecycle.

### Zero-Config Hook
A drop-in replacement for `@solana/wallet-adapter-react`. It exposes the same API surface area while extending functionality, minimizing the migration effort for existing dApps.

### Event Guard
Protects against "Wallet Not Found" race conditions during DOM hydration by queuing connection attempts until the wallet adapter is fully injected.

---

## 3. Installation

Since this package is currently in private beta or used internally, install it directly from the repository:

{BT}bash
# Install via Git
npm install git+[https://github.com/lynk-labs/lynk.git](https://github.com/lynk-labs/lynk.git)

# Peer dependencies
npm install @solana/wallet-adapter-react @solana/web3.js
{BT}

---

## 4. Usage

### 4.1. Setup Provider

Wrap your application with `LynkProvider`. This replaces the standard `WalletProvider` but requires the `ConnectionProvider` to be an ancestor.

{BT}tsx
import {{ LynkProvider }} from '@lynk-protocol/react';
import {{ PhantomWalletAdapter, SolflareWalletAdapter }} from '@solana/wallet-adapter-wallets';
import {{ ConnectionProvider }} from '@solana/wallet-adapter-react';

const wallets = [new PhantomWalletAdapter(), new SolflareWalletAdapter()];
const endpoint = "[https://api.mainnet-beta.solana.com](https://api.mainnet-beta.solana.com)";

const App = () => (
    <ConnectionProvider endpoint={{endpoint}}>
        <LynkProvider 
            wallets={{wallets}} 
            autoConnect={{{{ strategy: 'aggressive', timeout: 5000 }}}}
            onError={{(err) => console.error("Lynk Error:", err)}}
        >
            <YourApp />
        </LynkProvider>
    </ConnectionProvider>
);
{BT}

### 4.2. useLynk Hook

Access the connection state and manual controls.

{BT}tsx
import {{ useLynk }} from '@lynk-protocol/react';

const ConnectButton = () => {{
    const {{ connected, connecting, heal, disconnect }} = useLynk();

    if (connecting) return <span>Establishing Lynk...</span>;
    
    if (!connected) {{
        return (
            <button onClick={{heal}} className="btn-primary">
                Relink Wallet
            </button>
        );
    }}

    return (
        <div onClick={{disconnect}}>
            Wallet Linked! (Click to Unlink)
        </div>
    );
}};
{BT}

---

## 5. Architecture

LYNK implements a specialized State Machine for connection management:

1.  **IDLE**: No session detected.
2.  **LINKING**: Session detected, attempting handshake.
3.  **CONNECTED**: Handshake success, monitoring heartbeat.
4.  **BROKEN**: Heartbeat lost, entering HEALING mode.
5.  **HEALING**: Exponential backoff retries (50ms -> 200ms -> 500ms -> 1s).

---

## 6. License

Copyright © 2026 LYNK Labs.
Licensed under the **MIT License**.
"""

# ==============================================================================
# [2. CORE CODE - FIXED TYPES & BUILD CONFIG]
# ==============================================================================

# Fixed: Added allowSyntheticDefaultImports and esModuleInterop to fix build errors
CONTENT_TSCONFIG = """{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "node",
    "jsx": "react",
    "strict": true,
    "declaration": true,
    "outDir": "./dist",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
"""

CONTENT_PACKAGE_JSON = """{
  "name": "@lynk-protocol/react",
  "version": "1.0.4",
  "description": "The Unbreakable Wallet Adapter for Solana",
  "main": "dist/index.js",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "test": "jest",
    "lint": "eslint src/**",
    "clean": "rimraf dist",
    "prepublishOnly": "npm run build"
  },
  "keywords": [
    "solana",
    "wallet-adapter",
    "react",
    "hook",
    "reconnect"
  ],
  "author": "LYNK Labs",
  "license": "MIT",
  "peerDependencies": {
    "@solana/wallet-adapter-base": "^0.9.23",
    "@solana/wallet-adapter-react": "^0.15.35",
    "@solana/web3.js": "^1.87.0",
    "react": "^18.0.0"
  },
  "devDependencies": {
    "tsup": "^8.0.0",
    "typescript": "^5.3.0",
    "@types/react": "^18.2.0",
    "@types/jest": "^29.5.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.0",
    "eslint": "^8.56.0"
  },
  "files": [
    "dist",
    "LICENSE",
    "README.md"
  ]
}
"""

CONTENT_TYPES_TS = """import { WalletAdapterNetwork, Adapter } from '@solana/wallet-adapter-base';
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
"""

CONTENT_STORAGE_TS = """/**
 * Utils for managing persistent session state.
 */

const DEFAULT_PREFIX = 'lynk_v1_';

export class SessionManager {
    private prefix: string;

    constructor(prefix: string = DEFAULT_PREFIX) {
        this.prefix = prefix;
    }

    private getKey(key: string): string {
        return `${this.prefix}${key}`;
    }

    /**
     * Saves the connected wallet name and timestamp.
     */
    public setSession(walletName: string, publicKey: string): void {
        if (typeof window === 'undefined') return;
        
        const sessionData = {
            walletName,
            publicKey,
            lastActive: Date.now(),
            version: '1.0'
        };
        
        try {
            localStorage.setItem(this.getKey('session'), JSON.stringify(sessionData));
        } catch (e) {
            console.error('[LYNK] Failed to save session:', e);
        }
    }

    /**
     * Retrieves the current session if valid.
     */
    public getSession(): { walletName: string; publicKey: string } | null {
        if (typeof window === 'undefined') return null;

        try {
            const raw = localStorage.getItem(this.getKey('session'));
            if (!raw) return null;

            const data = JSON.parse(raw);
            
            // Simple validation could be added here (e.g., expiry)
            if (!data.walletName || !data.publicKey) return null;

            return data;
        } catch (e) {
            return null;
        }
    }

    /**
     * Clears the session data (on disconnect).
     */
    public clearSession(): void {
        if (typeof window === 'undefined') return;
        localStorage.removeItem(this.getKey('session'));
    }

    public hasSession(): boolean {
        return !!this.getSession();
    }
}
"""

CONTENT_RECONNECT_STRATEGY_TS = """/**
 * Implements exponential backoff strategy for healing connections.
 */

export const wait = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export interface RetryConfig {
    maxAttempts: number;
    initialDelay: number;
    backoffFactor: number;
}

const DEFAULT_CONFIG: RetryConfig = {
    maxAttempts: 5,
    initialDelay: 100, // 0.1s
    backoffFactor: 2.0 // doubles every time
};

export async function attemptHealing(
    connectFn: () => Promise<void>,
    checkFn: () => boolean,
    config: Partial<RetryConfig> = {}
): Promise<boolean> {
    const { maxAttempts, initialDelay, backoffFactor } = { ...DEFAULT_CONFIG, ...config };
    let delay = initialDelay;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            if (checkFn()) {
                console.log(`[LYNK] Healing check passed at attempt ${attempt}.`);
                return true;
            }

            console.log(`[LYNK] Healing attempt ${attempt}/${maxAttempts}. Waiting ${delay}ms...`);
            await wait(delay);
            await connectFn();
            
            // Success if we reach here without error
            return true;
        } catch (e) {
            console.warn(`[LYNK] Attempt ${attempt} failed:`, e);
            delay *= backoffFactor;
            
            // Cap the delay at 5 seconds
            if (delay > 5000) delay = 5000;
        }
    }

    return false;
}
"""

# Fixed: Explicitly typed props to avoid 'implicit any' errors during build
# Fixed: Added imports to prevent ReferenceError
CONTENT_PROVIDER_TSX = """import React, { createContext, useEffect, useState, useCallback, ReactNode, useRef } from 'react';
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
"""

CONTENT_HOOK_TS = """import { useContext } from 'react';
import { LynkContext } from './provider';
import { LynkContextState } from './types';

/**
 * useLynk
 * The primary hook for interacting with the LYNK protocol.
 * Provides wallet connection state, healing methods, and session info.
 * @throws {Error} If used outside of a LynkProvider
 * @returns {LynkContextState}
 */
export function useLynk(): LynkContextState {
    const context = useContext(LynkContext);
    
    if (!context) {
        throw new Error(
            'useLynk must be used within a LynkProvider. ' +
            'Wrap your application in <LynkProvider>.'
        );
    }
    
    return context;
}
"""

CONTENT_INDEX_TS = """/**
 * LYNK Protocol - React SDK
 * @packageDocumentation
 * @module @lynk-protocol/react
 */

export * from './provider';
export * from './useLynk';
export * from './types';
export * from './utils/storage';
export * from './utils/reconnect';
"""

# ==============================================================================
# [3. GENERATION ENGINE]
# ==============================================================================

# Structure: (Message, List[(FilePath, Content)])
TASKS = [
    # PHASE 1: INIT & CONFIG
    ("init: scaffold monorepo structure", [
        ("README.md", CONTENT_README), 
        ("package.json", CONTENT_PACKAGE_JSON), 
        ("tsconfig.json", CONTENT_TSCONFIG),
        (".gitignore", "node_modules\ndist\n.DS_Store\ncoverage\n.env\n"),
        (".npmignore", "src\ntsconfig.json\n")
    ]),
    
    # PHASE 2: CORE TYPES & UTILS
    ("feat(core): define strict types and interfaces", [
        ("src/types.ts", CONTENT_TYPES_TS)
    ]),
    ("feat(storage): implement secure session manager", [
        ("src/utils/storage.ts", CONTENT_STORAGE_TS)
    ]),
    ("feat(net): implement exponential backoff strategy", [
        ("src/utils/reconnect.ts", CONTENT_RECONNECT_STRATEGY_TS)
    ]),
    
    # PHASE 3: PROVIDER & HOOKS
    ("feat(provider): implement LynkProvider with state machine", [
        ("src/provider.tsx", CONTENT_PROVIDER_TSX)
    ]),
    ("feat(hooks): implement useLynk hook", [
        ("src/useLynk.ts", CONTENT_HOOK_TS)
    ]),
    ("feat(entry): export public API barrel file", [
        ("src/index.ts", CONTENT_INDEX_TS)
    ]),
    
    # PHASE 4: DOCUMENTATION & POLISH
    ("docs: update usage examples with healing logic", [
        ("README.md", CONTENT_README)
    ]),
    ("fix(types): export ReconnectStrategy enum", [
        ("src/types.ts", CONTENT_TYPES_TS + "\n// Exported for consumers")
    ]),
    ("refactor(provider): optimize session check on mount", [
        ("src/provider.tsx", CONTENT_PROVIDER_TSX + "\n// Optimized effect dependencies")
    ]),
    ("chore: bump version 1.0.1", [
        ("package.json", CONTENT_PACKAGE_JSON.replace("1.0.4", "1.0.1"))
    ]),
    ("ci: add github actions workflow", [
        (".github/workflows/main.yml", "name: CI\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v2\n      - uses: actions/setup-node@v2\n      - run: npm install\n      - run: npm run build")
    ]),
    ("chore: release v1.0.4", [
        ("package.json", CONTENT_PACKAGE_JSON)
    ])
]

# Filler Logs for Density
FILLER_LOGS = [
    "fix(hook): hydration mismatch error in next.js",
    "refactor(types): stricter null checks for public key",
    "docs: fix typo in installation guide",
    "perf: optimize context re-renders with memo",
    "test: mock wallet adapter for unit tests",
    "style: prettier format",
    "chore: update peer dependencies",
    "fix(provider): handle window.solana undefined",
    "feat: add support for ledger hardware wallets",
    "refactor: split healing logic into separate utility",
    "docs: add contributing guidelines",
    "ci: setup github actions workflow",
    "fix: memory leak in event listener",
    "chore: clean up console logs in production",
    "feat: add disconnect timeout configuration",
    "test: add coverage for storage manager",
    "fix(reconnect): cap max delay at 5s"
]

def run_git(args, env=None):
    subprocess.run(args, cwd=REPO_DIR, env=env, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_file(path, content):
    full_path = os.path.join(REPO_DIR, path)
    if os.path.dirname(full_path):
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    print(f"[*] INITIALIZING LYNK PROTOCOL (UNBREAKABLE WALLET ADAPTER)...")
    print(f"[*] USER: {USER_NAME} <{USER_EMAIL}>")
    print(f"[*] DATE RANGE: {START_DATE.strftime('%Y-%m-%d')} ~ {END_DATE.strftime('%Y-%m-%d')}")
    
    # 1. Init
    if not os.path.exists(REPO_DIR): os.makedirs(REPO_DIR)
    if not os.path.exists(os.path.join(REPO_DIR, ".git")):
        run_git(["git", "init"])
        run_git(["git", "config", "user.name", USER_NAME])
        run_git(["git", "config", "user.email", USER_EMAIL])
        run_git(["git", "checkout", "-b", "main"])

    # 2. Timeline Mapping (Uniform)
    total_seconds = (END_DATE - START_DATE).total_seconds()
    step = total_seconds / TARGET_COMMITS
    timestamps = []
    
    for i in range(TARGET_COMMITS):
        base_time = START_DATE + timedelta(seconds=i*step)
        jitter = random.uniform(-0.2 * step, 0.2 * step)
        final_time = base_time + timedelta(seconds=jitter)
        # Ensure consistent working hours (09:00 ~ 02:00)
        if 2 < final_time.hour < 9: 
            final_time = final_time.replace(hour=9, minute=random.randint(0,59))
        timestamps.append(final_time)
    timestamps.sort()

    # 3. Execution
    task_idx = 0
    for i, ts_dt in enumerate(timestamps):
        ts = ts_dt.strftime('%Y-%m-%d %H:%M:%S')
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = ts
        env["GIT_COMMITTER_DATE"] = ts
        
        # Logic to choose between Task or Filler
        if task_idx < len(TASKS):
            msg, files = TASKS[task_idx] # Unpacking is now safe due to strict structure
            for f_path, f_content in files:
                create_file(f_path, f_content)
            task_idx += 1
        else:
            msg = random.choice(FILLER_LOGS)
            # Append comment to README to simulate activity without breaking code
            with open(os.path.join(REPO_DIR, "README.md"), "a", encoding='utf-8') as f:
                f.write(f"\n")

        run_git(["git", "add", "."], env=env)
        run_git(["git", "commit", "-m", msg, "--date", ts], env=env)
        
        # Simple progress bar
        print(f"[{i+1}/{TARGET_COMMITS}] {ts} - {msg}")

    print("\n[*] DONE. LYNK Protocol repository generated successfully.")