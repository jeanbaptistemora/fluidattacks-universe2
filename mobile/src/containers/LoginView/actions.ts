import { Google } from "expo";
import { ToastAndroid } from "react-native";

import { ThunkDispatcher, ThunkResult } from "../../store";
import { GOOGLE_LOGIN_KEY } from "../../utils/constants";

export enum actionTypes {
  GOOGLE_LOGIN_LOAD = "login/google/load",
  GOOGLE_LOGIN_SUCCESS = "login/google/success",
}

export const performAsyncGoogleLogin: (() => ThunkResult<void>) = (): ThunkResult<void> => (
  dispatch: ThunkDispatcher,
): void => {
  dispatch({ payload: {}, type: actionTypes.GOOGLE_LOGIN_LOAD });
  Google.logInAsync({
    androidClientId: GOOGLE_LOGIN_KEY,
    scopes: ["profile", "email"],
  })
    .then((result: Google.LogInResult) => {
      if (result.type === "success") {
        dispatch({ payload: { userInfo: result.user }, type: actionTypes.GOOGLE_LOGIN_SUCCESS });
      }
    })
    .catch((error: Error) => {
      ToastAndroid.show("Oops! There is an error.", ToastAndroid.SHORT);
      throw error;
    });
};
