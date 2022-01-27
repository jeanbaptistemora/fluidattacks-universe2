/* eslint-disable fp/no-let,fp/no-mutation
  --------
  Used to be able to generate and assign a secret key, every time its useful life expires.
*/
import _ from "lodash";
import { track } from "mixpanel-browser";
import type React from "react";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { random, decrypt as sjclDecrypt, encrypt as sjclEncrypt } from "sjcl";

import { Logger } from "utils/logger";

const msInSecond: number = 1000;
const secondsInMinute = 60;
const sessionAgeInMinutes: number = 40;
const secretsLifespan: number = secondsInMinute * sessionAgeInMinutes;
const secretsLifespanInMiliseconds: number = secretsLifespan * msInSecond;

const wordsNumber: number = 8;

// Secret
let secretKey: sjcl.BitArray = random.randomWords(wordsNumber);

function generateSecrets(): void {
  secretKey = random.randomWords(wordsNumber);
}

// Rotation
setInterval(generateSecrets, secretsLifespanInMiliseconds);

function decrypt(ciphertext: string): string {
  return sjclDecrypt(secretKey, JSON.parse(ciphertext));
}

function encrypt(plaintext: string): string {
  return JSON.stringify(sjclEncrypt(secretKey, plaintext));
}

// Wrapper for React.useState that persists using the Web Storage API
function useStoredState<T>(
  key: string,
  defaultValue: T,
  storageProvider: Readonly<Storage> = sessionStorage,
  encrypted: boolean = false
): readonly [T, React.Dispatch<React.SetStateAction<T>>] {
  function parseDecrypt(value: string): T {
    try {
      return JSON.parse(decrypt(value)) as T;
    } catch (exception: unknown) {
      return defaultValue;
    }
  }
  const loadInitialState: () => T = (): T => {
    const storedState: string | null = storageProvider.getItem(key);

    return _.isNull(storedState)
      ? defaultValue
      : encrypted
      ? parseDecrypt(storedState)
      : (JSON.parse(storedState) as T);
  };

  const [state, setState] = useState<T>(loadInitialState);

  const setAndStore: React.Dispatch<React.SetStateAction<T>> = (
    value: React.SetStateAction<T>
  ): void => {
    try {
      storageProvider.setItem(
        key,
        encrypted
          ? encrypt(
              JSON.stringify(value instanceof Function ? value(state) : value)
            )
          : JSON.stringify(value instanceof Function ? value(state) : value)
      );
    } catch (exception: unknown) {
      Logger.warning("Couldn't persist state to web storage", exception);
    }
    setState(value);
  };

  return [state, setAndStore] as const;
}

// Calls mixpanel track on route change
const useTabTracking: (containerName: string) => void = (
  containerName
): void => {
  const { pathname } = useLocation();

  useEffect((): void => {
    const lastElements: number = -2;
    const [id, tabName] = pathname.split("/").slice(lastElements);

    if (tabName && tabName.toLowerCase() !== containerName.toLowerCase()) {
      track(`${containerName}${_.capitalize(tabName)}`, { id });
    } else {
      track(containerName);
    }
  }, [containerName, pathname]);
};

export { useStoredState, useTabTracking };
