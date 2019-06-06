import { MutationResult } from "react-apollo";
import { RouteComponentProps } from "react-router-native";

import { ILoginState } from "../LoginView/reducer";

export type IWelcomeProps = RouteComponentProps<{}, {}, {
  authProvider: string;
  authToken: string;
  pushToken: string;
  userInfo: ILoginState["userInfo"];
}>;

export type SIGN_IN_RESULT = MutationResult<{
  signIn: {
    authorized: boolean;
    sessionJwt: string;
    success: boolean;
  };
}>["data"];
