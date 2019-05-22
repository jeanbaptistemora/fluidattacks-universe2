import { Action, applyMiddleware, createStore, Store } from "redux";
import thunk, { ThunkAction, ThunkDispatch } from "redux-thunk";

import { ILoginState } from "../containers/LoginView/reducer";

import { rootReducer } from "./rootReducer";

/**
 * State structure of the whole app
 */
export interface IState {
  login: ILoginState;
}

/**
 * Redux action object content
 */
export interface IActionStructure extends Action<string> {
  payload: Dictionary;
}

export type ThunkDispatcher = ThunkDispatch<IState, undefined, IActionStructure>;
export type ThunkResult<T> = ThunkAction<T, IState, undefined, IActionStructure>;

export const store: Store<IState, IActionStructure> = createStore(
  rootReducer,
  applyMiddleware(thunk),
);
