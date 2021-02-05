import React from "react";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import { useLocation } from "react-router";

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

  const [state, setState] = React.useState<T>(loadInitialState);

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
  const location: ReturnType<typeof useLocation> = useLocation();

  React.useEffect((): void => {
    const tab: string = _.last(location.pathname.split("/")) as string;
    mixpanel.track(`${containerName}${_.capitalize(tab)}`);
  }, [containerName, location]);
};

export { useStoredState, useTabTracking };
