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
  setTimeout((): void => {
    // eslint-disable-next-line no-alert -- Deliberate usage
    alert(translate.t("validations.validSessionDate"));
    location.replace(`https://${window.location.host}`);
  }, utc(expDate).diff(utc()));
};

export { authContext, IAuthContext, setupSessionCheck };
