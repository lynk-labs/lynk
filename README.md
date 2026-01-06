# LYNK: The Unbreakable Wallet Adapter

<div align="center">
  <img src="./lynk.png" alt="LYNK Banner" width="100%" />
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

```bash
# Install via Git
npm install git+[https://github.com/lynk-labs/lynk.git](https://github.com/lynk-labs/lynk.git)

# Peer dependencies
npm install @solana/wallet-adapter-react @solana/web3.js
```

---

## 4. Usage

### 4.1. Setup Provider

Wrap your application with `LynkProvider`. This replaces the standard `WalletProvider` but requires the `ConnectionProvider` to be an ancestor.

```tsx
import { LynkProvider } from '@lynk-protocol/react';
import { PhantomWalletAdapter, SolflareWalletAdapter } from '@solana/wallet-adapter-wallets';
import { ConnectionProvider } from '@solana/wallet-adapter-react';

const wallets = [new PhantomWalletAdapter(), new SolflareWalletAdapter()];
const endpoint = "[https://api.mainnet-beta.solana.com](https://api.mainnet-beta.solana.com)";

const App = () => (
    <ConnectionProvider endpoint={endpoint}>
        <LynkProvider 
            wallets={wallets} 
            autoConnect={{ strategy: 'aggressive', timeout: 5000 }}
            onError={(err) => console.error("Lynk Error:", err)}
        >
            <YourApp />
        </LynkProvider>
    </ConnectionProvider>
);
```

### 4.2. useLynk Hook

Access the connection state and manual controls.

```tsx
import { useLynk } from '@lynk-protocol/react';

const ConnectButton = () => {
    const { connected, connecting, heal, disconnect } = useLynk();

    if (connecting) return <span>Establishing Lynk...</span>;
    
    if (!connected) {
        return (
            <button onClick={heal} className="btn-primary">
                Relink Wallet
            </button>
        );
    }

    return (
        <div onClick={disconnect}>
            Wallet Linked! (Click to Unlink)
        </div>
    );
};
```

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





























































































