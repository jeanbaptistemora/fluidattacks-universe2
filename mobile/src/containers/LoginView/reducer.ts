import { Reducer } from "redux";

import { IActionStructure } from "../../store";

import { actionTypes } from "./actions";

/**
 * State structure of LoginView
 */
export interface ILoginState {
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
}

export const initialState: ILoginState = {
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
};

const actionMap: Dictionary<((state: ILoginState, action: IActionStructure) => ILoginState)> = {};

actionMap[actionTypes.GOOGLE_LOGIN_LOAD] = (state: ILoginState): ILoginState => ({
  ...state,
  isLoading: !state.isLoading,
});

actionMap[actionTypes.GOOGLE_LOGIN_SUCCESS] = (state: ILoginState, action: IActionStructure): ILoginState => ({
  ...state,
  isAuthenticated: true,
  userInfo: action.payload.userInfo as ILoginState["userInfo"],
});

export const loginReducer: Reducer<ILoginState, IActionStructure> = (
  state: ILoginState = initialState, action: IActionStructure,
): ILoginState => {
  if (action.type in actionMap) {
    return actionMap[action.type](state, action);
  }

  return state;
};
