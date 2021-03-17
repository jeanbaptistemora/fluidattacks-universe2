import type React from "react";
import _ from "lodash";
import { track } from "mixpanel-browser";
import { useLocation } from "react-router";
import { useEffect, useState } from "react";

// Wrapper for React.useState that persists using the Web Storage API
function useStoredState<T>(
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

  const [state, setState] = useState<T>(loadInitialState);

  const setAndStore: React.Dispatch<React.SetStateAction<T>> = (
    value: React.SetStateAction<T>
  ): void => {
    storageProvider.setItem(key, JSON.stringify(value));
    setState(value);
  };

  return [state, setAndStore] as const;
}

const useTabTracking: (containerName: string) => void = (
  containerName
): void => {
  const { pathname } = useLocation();

  useEffect((): void => {
    const lastElements: number = -2;
    const [id, tabName] = pathname.split("/").slice(lastElements);

    if (tabName) {
      track(`${containerName}${_.capitalize(tabName)}`, { id });
    }
  }, [containerName, pathname]);
};

export { useStoredState, useTabTracking };
