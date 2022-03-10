import _ from "lodash";
import { track } from "mixpanel-browser";
import { useEffect } from "react";
import { useLocation } from "react-router-dom";

// Calls mixpanel track on route change
const useTabTracking = (containerName: string): void => {
  const { pathname } = useLocation();

  useEffect((): void => {
    const lastElements = -2;
    const [id, tabName] = pathname.split("/").slice(lastElements);

    if (tabName && tabName.toLowerCase() !== containerName.toLowerCase()) {
      track(`${containerName}${_.capitalize(tabName)}`, { id });
    } else {
      track(containerName);
    }
  }, [containerName, pathname]);
};

export { useTabTracking };
