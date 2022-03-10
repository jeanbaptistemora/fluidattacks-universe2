/* eslint-disable fp/no-let,fp/no-mutation
  --------
  Used to be able to generate and assign a secret key, every time its useful life expires.
*/
import _ from "lodash";
import type React from "react";
import { useState } from "react";
import { random, decrypt as sjclDecrypt, encrypt as sjclEncrypt } from "sjcl";

import { Logger } from "utils/logger";

const msInSecond = 1000;
const secondsInMinute = 60;
const sessionAgeInMinutes = 40;
const secretsLifespan = secondsInMinute * sessionAgeInMinutes;
const secretsLifespanInMiliseconds = secretsLifespan * msInSecond;

const wordsNumber = 8;

// Secret
let secretKey = random.randomWords(wordsNumber);

const generateSecrets = (): void => {
  secretKey = random.randomWords(wordsNumber);
};

// Rotation
setInterval(generateSecrets, secretsLifespanInMiliseconds);

const decrypt = (ciphertext: string): string => {
  return sjclDecrypt(secretKey, JSON.parse(ciphertext));
};

const encrypt = (plaintext: string): string => {
  return JSON.stringify(sjclEncrypt(secretKey, plaintext));
};

// Wrapper for React.useState that persists using the Web Storage API
const useStoredState = <T>(
  key: string,
  defaultValue: T,
  storageProvider: Readonly<Storage> = sessionStorage,
  encrypted: boolean = false
): [T, React.Dispatch<React.SetStateAction<T>>] => {
  const parseDecrypt = (value: string): T => {
    try {
      return JSON.parse(decrypt(value)) as T;
    } catch (exception: unknown) {
      return defaultValue;
    }
  };
  const loadInitialState = (): T => {
    const storedState = storageProvider.getItem(key);

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

  return [state, setAndStore];
};

export { useStoredState };
