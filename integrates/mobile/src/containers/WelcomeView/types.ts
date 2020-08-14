/**
 * Sign in mutation response
 */
export interface ISignInResult {
  signIn: {
    sessionJwt: string;
    success: boolean;
  };
}
