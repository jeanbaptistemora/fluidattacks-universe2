import _ from "lodash";
import React from "react";

// Wrapper for React.useState that persists using the Web Storage API
type StoredStateHook = <T>(
  key: string,
  defaultValue: T,
  storageProvider?: Storage,
) => [T, React.Dispatch<React.SetStateAction<T>>];

export const useStoredState: StoredStateHook = <T>(
  key: string,
  defaultValue: T,
  storageProvider: Storage = sessionStorage,
): [T, React.Dispatch<React.SetStateAction<T>>] => {

  const loadInitialState: (() => T) = (): T => {
    const storedState: string | null = storageProvider.getItem(key);

    return storedState === null
      ? defaultValue
      : _.isObject(defaultValue)
        ? JSON.parse(storedState)
        : storedState;
  };

  const [state, setState] = React.useState<T>(loadInitialState);

  const setAndStore: React.Dispatch<React.SetStateAction<T>> = (value: React.SetStateAction<T>): void => {
    const parsedValue: string = _.isString(value)
      ? value
      : JSON.stringify(value);

    storageProvider.setItem(key, parsedValue);
    setState(value);
  };

  return [state, setAndStore];
};
