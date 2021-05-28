import _ from "lodash";
import { track } from "mixpanel-browser";
import type React from "react";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

import { Logger } from "utils/logger";

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
    try {
      storageProvider.setItem(
        key,
        JSON.stringify(value instanceof Function ? value(state) : value)
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

    if (tabName) {
      track(`${containerName}${_.capitalize(tabName)}`, { id });
    }
  }, [containerName, pathname]);
};

export { useStoredState, useTabTracking };
