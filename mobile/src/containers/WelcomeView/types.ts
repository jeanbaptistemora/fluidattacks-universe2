import { GoogleUser } from "expo-google-app-auth";

/**
 * Social auth response
 */
export interface IAuthResult {
  authProvider: string;
  authToken: string;
  pushToken: string;
  userInfo: GoogleUser;
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
