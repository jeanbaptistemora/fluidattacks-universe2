import { Reducer } from "redux";

import { IActionStructure } from "../../store";

import { actionTypes } from "./actions";

/**
 * State structure of LoginView
 */
export interface ILoginState {
  authProvider: string;
  authToken: string;
  isAuthenticated: boolean;
  isLoading: boolean;
  userInfo: {
    email?: string;
    familyName: string;
    givenName: string;
    id: string;
    name: string;
    photoUrl?: string;
  };
  versionStatus?: checkResult;
}

export const initialState: ILoginState = {
  authProvider: "",
  authToken: "",
  isAuthenticated: false,
  isLoading: false,
  userInfo: {
    email: "",
    familyName: "",
    givenName: "",
    id: "",
    name: "",
    photoUrl: "",
  },
  versionStatus: undefined,
};

const actionMap: Dictionary<((state: ILoginState, action: IActionStructure) => ILoginState)> = {};

actionMap[actionTypes.GOOGLE_LOGIN_LOAD] = (state: ILoginState): ILoginState => ({
  ...state,
  isLoading: !state.isLoading,
});

actionMap[actionTypes.LOGIN_SUCCESS] = (state: ILoginState, action: IActionStructure): ILoginState => ({
  ...state,
  authProvider: action.payload.authProvider as string,
  authToken: action.payload.authToken as string,
  isAuthenticated: true,
  userInfo: action.payload.userInfo as ILoginState["userInfo"],
});

actionMap[actionTypes.RESOLVE_VERSION] = (state: ILoginState, action: IActionStructure): ILoginState => ({
  ...state,
  versionStatus: action.payload.status as checkResult,
});

export const loginReducer: Reducer<ILoginState, IActionStructure> = (
  state: ILoginState = initialState, action: IActionStructure,
): ILoginState => {
  if (action.type in actionMap) {
    return actionMap[action.type](state, action);
  }

  return state;
};
