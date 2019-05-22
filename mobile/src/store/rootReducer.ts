import { combineReducers, Reducer } from "redux";

import { loginReducer } from "../containers/LoginView/reducer";

import { IActionStructure, IState } from "./index";

export const rootReducer: Reducer<IState, IActionStructure> = combineReducers({
  login: loginReducer,
});
