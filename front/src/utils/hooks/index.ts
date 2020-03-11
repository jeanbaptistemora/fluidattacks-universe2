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

  const [state, setState] = React.useState<T>(
    (): T => JSON.parse(_.get(storageProvider, key, defaultValue)),
  );

  const setAndStore: React.Dispatch<React.SetStateAction<T>> = (value: React.SetStateAction<T>): void => {
    storageProvider.setItem(key, JSON.stringify(value));
    setState(value);
  };

  return [state, setAndStore];
};
