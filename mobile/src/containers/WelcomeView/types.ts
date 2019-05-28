import { MutationResult } from "react-apollo";
import { RouteComponentProps } from "react-router-native";

import { ILoginState } from "../LoginView/reducer";

export type IWelcomeProps = RouteComponentProps<{}, {}, {
  authProvider: string;
  authToken: string;
  userInfo: ILoginState["userInfo"];
}>;

export type SIGN_IN_RESULT = MutationResult<{
  signIn: {
    sessionJwt: string;
    success: boolean;
  };
}>["data"];
