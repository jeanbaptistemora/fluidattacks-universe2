import { Google, Notifications } from "expo";
import * as Permissions from "expo-permissions";

import { IActionStructure, ThunkDispatcher, ThunkResult } from "../../store";
import {
  GOOGLE_LOGIN_KEY_ANDROID_DEV,
  GOOGLE_LOGIN_KEY_ANDROID_PROD,
  GOOGLE_LOGIN_KEY_IOS_DEV,
  GOOGLE_LOGIN_KEY_IOS_PROD,
} from "../../utils/constants";
import * as errorDialog from "../../utils/errorDialog";
import { rollbar } from "../../utils/rollbar";

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
    androidClientId: GOOGLE_LOGIN_KEY_ANDROID_DEV,
    androidStandaloneAppClientId: GOOGLE_LOGIN_KEY_ANDROID_PROD,
    clientId: "",
    iosClientId: GOOGLE_LOGIN_KEY_IOS_DEV,
    iosStandaloneAppClientId: GOOGLE_LOGIN_KEY_IOS_PROD,
    scopes: ["profile", "email"],
  })
    .then(async (result: Google.LogInResult): Promise<void> => {
      dispatch({ payload: {}, type: actionTypes.GOOGLE_LOGIN_LOAD });
      if (result.type === "success") {
        const { status: notifPermission } = await Permissions.getAsync(Permissions.NOTIFICATIONS);

        dispatch({
          payload: {
            authProvider: "google",
            authToken: String(result.idToken),
            pushToken: notifPermission === "granted" ? await Notifications.getExpoPushTokenAsync() : "",
            userInfo: result.user,
          },
          type: actionTypes.LOGIN_SUCCESS,
        });
      } else {
        // User canceled the operation
      }
    })
    .catch((error: Error) => {
      errorDialog.show();
      rollbar.error("Error: An error occurred authenticating with Google", error);
    });
};

export const resolveVersion: ((isOutdated: boolean) => IActionStructure) = (isOutdated: boolean): IActionStructure => ({
  payload: { isOutdated },
  type: actionTypes.RESOLVE_VERSION,
});
