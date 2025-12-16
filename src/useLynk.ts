import { useContext } from 'react';
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
