/**
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
