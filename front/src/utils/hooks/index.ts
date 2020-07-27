import React from "react";
import _ from "lodash";

// Wrapper for React.useState that persists using the Web Storage API
export function useStoredState<T>(
  key: string,
  defaultValue: T,
  storageProvider: Readonly<Storage> = sessionStorage
): readonly [T, React.Dispatch<React.SetStateAction<T>>] {
  const loadInitialState: () => T = (): T => {
    const storedState: string | null = storageProvider.getItem(key);

    return _.isNull(storedState)
      ? defaultValue
      : (JSON.parse(storedState) as T);
  };

  const [state, setState] = React.useState<T>(loadInitialState);

  const setAndStore: React.Dispatch<React.SetStateAction<T>> = (
    value: React.SetStateAction<T>
  ): void => {
    storageProvider.setItem(key, JSON.stringify(value));
    setState(value);
  };

  return [state, setAndStore] as const;
}
