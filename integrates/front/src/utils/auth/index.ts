import { utc } from "moment";
import type React from "react";
import { createContext } from "react";

import { translate } from "utils/translations/translate";

interface IUser {
  userEmail: string;
  userName: string;
}

interface IAuthContext extends IUser {
  setUser?: React.Dispatch<React.SetStateAction<IUser>>;
}

const authContext: React.Context<IAuthContext> = createContext({
  userEmail: "",
  userName: "",
});

const setupSessionCheck: (expDate: string) => void = (expDate): void => {
  const state: { active: boolean; timerId: number } = {
    active: true,
    timerId: 0,
  };

  const startInactivityTimer: () => number = (): number => {
    const msInSec: number = 1000;
    const timeout: number = 1200;

    return window.setTimeout((): void => {
      // eslint-disable-next-line fp/no-mutation
      state.active = false;
      // eslint-disable-next-line no-alert -- Deliberate usage
      alert(translate.t("validations.inactiveSession"));
      location.replace("/logout");
    }, timeout * msInSec);
  };

  // eslint-disable-next-line fp/no-mutation
  state.timerId = startInactivityTimer();
  const events: string[] = [
    "mousemove",
    "mousedown",
    "keypress",
    "DOMMouseScroll",
    "wheel",
    "touchmove",
    "MSPointerMove",
  ];
  events.forEach((item: string): void => {
    window.addEventListener(
      item,
      (): void => {
        // eslint-disable-next-line fp/no-mutation
        state.active = true;
        clearTimeout(state.timerId);
        // eslint-disable-next-line fp/no-mutation
        state.timerId = startInactivityTimer();
      },
      false
    );
  });

  setTimeout((): void => {
    if (!state.active) {
      // eslint-disable-next-line no-alert -- Deliberate usage
      alert(translate.t("validations.validSessionDate"));
    }
    location.replace(`https://${window.location.host}`);
  }, utc(expDate).diff(utc()));
};

export { authContext, IAuthContext, setupSessionCheck };
