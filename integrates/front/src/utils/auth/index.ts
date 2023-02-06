import dayjs, { extend } from "dayjs";
import utc from "dayjs/plugin/utc";
import type React from "react";
import { createContext } from "react";

import { translate } from "utils/translations/translate";

interface IUser {
  tours: {
    newGroup: boolean;
    newRiskExposure: boolean;
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
    newRiskExposure: false,
    newRoot: false,
  },
  userEmail: "",
  userName: "",
});

extend(utc);

const setupSessionCheck: (expDate: string) => void = (expDate): void => {
  setTimeout((): void => {
    location.replace("/logout");
    // eslint-disable-next-line no-alert -- Deliberate usage
    alert(translate.t("validations.validSessionDate"));
  }, dayjs.utc(expDate).diff(dayjs.utc()));
};

export type { IAuthContext };
export { authContext, setupSessionCheck };
