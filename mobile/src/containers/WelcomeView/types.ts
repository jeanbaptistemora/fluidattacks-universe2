import { IUser } from "../LoginView/socialAuth";

/**
 * Auth data provided after login
 */
export interface IAuthState {
  authProvider: string;
  authToken: string;
  user: IUser;
}

/**
 * Sign in mutation response
 */
export interface ISignInResult {
  signIn: {
    sessionJwt: string;
    success: boolean;
  };
}
