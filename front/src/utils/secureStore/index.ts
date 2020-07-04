import React from "react";
import sjcl from "sjcl";

/* Secrets declared in this file live as much as the dashboard tab is open
 * or this predefined lifespan
 */
const secretsLifespanInMiliseconds: number = 600 * 1000;

// Secrets
let secretKey: sjcl.BitArray;

// Secrets generation
const generateSecrets: () => void = (): void => {
  secretKey = sjcl.random.randomWords(8);
};

// Secrets rotation
generateSecrets();
setInterval(generateSecrets, secretsLifespanInMiliseconds);

// Implementation
const decrypt: (ciphertext: string) => string = (ciphertext: string): string => (
  sjcl.decrypt(secretKey, JSON.parse(ciphertext))
);

const encrypt: (plaintext: string) => string = (plaintext: string): string => (
  JSON.stringify(sjcl.encrypt(secretKey, plaintext))
);

const hash: (input: string) => string = (input: string) => (
  sjcl.codec.hex.fromBits(sjcl.hash.sha256.hash(input))
);

const storeBlob: (identifier: string, contents: string, mime: string) => boolean =
  (identifier: string, contents: string, mime: string): boolean => {
    let success: boolean;

    const blob: Blob = new Blob([contents], { type: mime });
    const url: string = URL
      .createObjectURL(blob)
      .toString();

    /* Revoke the url that points to the blob, and therefore the blob
     *   https://w3c.github.io/FileAPI/#creating-revoking
     */
    const revokeUrl: () => void = (): void => {
      URL.revokeObjectURL(url);
    };
    setTimeout(revokeUrl, secretsLifespanInMiliseconds);

    try {
      sessionStorage.setItem(hash(identifier), encrypt(url));
      success = true;
    } catch {
      success = false;
    }

    return success;
  };

const retrieveBlob: (identifier: string) => string | undefined =
  (identifier: string): string | undefined => {
    let result: string | undefined;
    const item: string = hash(identifier);

    try {
      const url: string | null = sessionStorage.getItem(item);
      result = url === null ? undefined : decrypt(url);
    } catch {
      result = undefined;
      sessionStorage.removeItem(item);
    }

    return result;
  };

export interface ISecureStore {
  decrypt(ciphertext: string): string;
  encrypt(plaintext: string): string;
  hash(input: string): string;
  retrieveBlob(identifier: string): string | undefined;
  storeBlob(identifier: string, contents: string, mime: string): boolean;
}

export const secureStore: ISecureStore = {
  decrypt,
  encrypt,
  hash,
  retrieveBlob,
  storeBlob,
};

export const secureStoreContext: React.Context<ISecureStore> = React.createContext(secureStore);
