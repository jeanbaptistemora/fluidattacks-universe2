import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import { useEffect } from "react";
import { useLocation } from "react-router-dom";

// Calls mixpanel track on route change
const useTabTracking = (containerName: string): void => {
  const { pathname } = useLocation();

  useEffect((): void => {
    const lastElements = -2;
    const [id, tabName] = pathname.split("/").slice(lastElements);

    if (tabName && tabName.toLowerCase() !== containerName.toLowerCase()) {
      mixpanel.track(`${containerName}${_.capitalize(tabName)}`, { id });
    } else {
      mixpanel.track(containerName);
    }
  }, [containerName, pathname]);
};

export { useTabTracking };
