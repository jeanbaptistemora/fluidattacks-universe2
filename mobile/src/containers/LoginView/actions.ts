import { Google, Notifications } from "expo";

import { IActionStructure, ThunkDispatcher, ThunkResult } from "../../store";
import { GOOGLE_LOGIN_KEY } from "../../utils/constants";
import * as errorDialog from "../../utils/errorDialog";

export enum actionTypes {
  GOOGLE_LOGIN_LOAD = "login/google/load",
  LOGIN_SUCCESS = "login/success",
  RESOLVE_VERSION = "login/version",
}

export const performAsyncGoogleLogin: (() => ThunkResult<void>) = (): ThunkResult<void> => (
  dispatch: ThunkDispatcher,
): void => {
  dispatch({ payload: {}, type: actionTypes.GOOGLE_LOGIN_LOAD });
  Google.logInAsync({
    androidClientId: GOOGLE_LOGIN_KEY,
    iosClientId: GOOGLE_LOGIN_KEY,
    scopes: ["profile", "email"],
  })
    .then(async (result: Google.LogInResult): Promise<void> => {
      dispatch({ payload: {}, type: actionTypes.GOOGLE_LOGIN_LOAD });
      if (result.type === "success") {
        dispatch({
          payload: {
            authProvider: "google",
            authToken: result.idToken,
            pushToken: await Notifications.getExpoPushTokenAsync(),
            userInfo: result.user,
          },
          type: actionTypes.LOGIN_SUCCESS,
        });
      }
    })
    .catch((error: Error) => {
      errorDialog.show();
      throw error;
    });
};

export const resolveVersion: ((isOutdated: boolean) => IActionStructure) = (isOutdated: boolean): IActionStructure => ({
  payload: { isOutdated },
  type: actionTypes.RESOLVE_VERSION,
});
