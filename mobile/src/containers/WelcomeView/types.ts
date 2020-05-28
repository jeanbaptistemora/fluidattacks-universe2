import { IUser } from "../LoginView/socialAuth";

/**
 * Auth data provided after login
 */
export interface IAuthState {
  authProvider: string;
  idToken: string;
  user: IUser;
}

/**
 * Sign in mutation response
 */
export interface ISignInResult {
  signIn: {
    authorized: boolean;
    sessionJwt: string;
    success: boolean;
  };
}
