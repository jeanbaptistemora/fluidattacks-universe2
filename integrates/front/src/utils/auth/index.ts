import { utc } from "moment";
import type React from "react";
import { createContext } from "react";

import { translate } from "utils/translations/translate";

interface IUser {
  tours: {
    newGroup: boolean;
    newRoot: boolean;
  };
  userEmail: string;
  userIntPhone?: string;
  userName: string;
}

interface IAuthContext extends IUser {
  setUser?: React.Dispatch<React.SetStateAction<IUser>>;
}

const authContext: React.Context<IAuthContext> = createContext<IAuthContext>({
  tours: {
    newGroup: false,
    newRoot: false,
  },
  userEmail: "",
  userName: "",
});

const setupSessionCheck: (expDate: string) => void = (expDate): void => {
  setTimeout((): void => {
    location.replace("/logout");
    // eslint-disable-next-line no-alert -- Deliberate usage
    alert(translate.t("validations.validSessionDate"));
  }, utc(expDate).diff(utc()));
};

export type { IAuthContext };
export { authContext, setupSessionCheck };
