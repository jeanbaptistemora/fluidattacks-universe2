/* eslint-disable fp/no-let,fp/no-mutation
  --------
  We need both to be able to generate and assign a secret key, every time its
  useful life expires.
*/
import Logger from "../logger";
import React from "react";
import sjcl from "sjcl";

/*
 * Secrets declared in this file live as much as the dashboard tab is open
 * or this predefined lifespan
 */
const secondsInMs: number = 1000;
const secretsLifespan: number = 600;
const secretsLifespanInMiliseconds: number = secretsLifespan * secondsInMs;

const wordsNumber: number = 8;

// Secrets
let secretKey: sjcl.BitArray = sjcl.random.randomWords(wordsNumber);

// Secrets generation
const generateSecrets: () => void = (): void => {
  secretKey = sjcl.random.randomWords(wordsNumber);
};

// Secrets rotation
setInterval(generateSecrets, secretsLifespanInMiliseconds);

// Type aliases
declare type iFrameReferenceType = React.MutableRefObject<HTMLIFrameElement | null>;

// Implementation
const decrypt: (ciphertext: string) => string = (ciphertext: string): string =>
  sjcl.decrypt(secretKey, JSON.parse(ciphertext));

const encrypt: (plaintext: string) => string = (plaintext: string): string =>
  JSON.stringify(sjcl.encrypt(secretKey, plaintext));

const hash: (input: string) => string = (input: string): string =>
  sjcl.codec.hex.fromBits(sjcl.hash.sha256.hash(input));

const storeBlob: (
  identifier: string,
  contents: string,
  mime: string
) => string = (identifier: string, contents: string, mime: string): string => {
  const blob: Blob = new Blob([contents], { type: mime });
  const itemName: string = hash(identifier);
  const url: string = URL.createObjectURL(blob).toString();

  /*
   * Revoke the url that points to the blob, and therefore the blob
   * https://w3c.github.io/FileAPI/#creating-revoking
   */
  const revokeUrl: () => void = (): void => {
    URL.revokeObjectURL(url);
  };
  setTimeout(revokeUrl, secretsLifespanInMiliseconds);

  try {
    sessionStorage.setItem(itemName, encrypt(url));
  } catch {
    revokeUrl();
  }

  return url;
};

const retrieveBlob: (identifier: string) => string = (
  identifier: string
): string => {
  let url: string | null = identifier;
  const itemName: string = hash(identifier);

  try {
    const itemValue: string | null = sessionStorage.getItem(itemName);
    url = itemValue === null ? identifier : decrypt(itemValue);
  } catch {
    sessionStorage.removeItem(itemName);
  }

  return url;
};

const storeIframeContent: (reference: Readonly<iFrameReferenceType>) => void = (
  reference: Readonly<iFrameReferenceType>
): void => {
  if (
    location.hostname === reference.current?.contentDocument?.location.hostname
  ) {
    const contents: string =
      reference.current.contentDocument.documentElement.outerHTML;
    const identifier: string | undefined =
      reference.current.contentWindow?.location.href;

    if (identifier !== undefined) {
      storeBlob(identifier, contents, "text/html");
    }
  } else {
    Logger.warning("Iframe with Cross-origin: Host != Iframe Host");
  }
};

export interface ISecureStoreConfig {
  decrypt: (ciphertext: string) => string;
  encrypt: (plaintext: string) => string;
  hash: (input: string) => string;
  retrieveBlob: (identifier: string) => string;
  storeBlob: (identifier: string, contents: string, mime: string) => string;
  storeIframeContent: (reference: Readonly<iFrameReferenceType>) => void;
}

export const secureStore: ISecureStoreConfig = {
  decrypt,
  encrypt,
  hash,
  retrieveBlob,
  storeBlob,
  storeIframeContent,
};

export const secureStoreContext: React.Context<ISecureStoreConfig> = React.createContext(
  secureStore
);
