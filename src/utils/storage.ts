/**
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
