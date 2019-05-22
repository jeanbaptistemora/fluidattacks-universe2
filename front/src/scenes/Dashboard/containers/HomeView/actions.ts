import { ThunkDispatch } from "redux-thunk";
import { IDashboardState } from "../../reducer";
import * as actionTypes from "./actionTypes";

export interface IActionStructure {
  payload?: { [key: string]: string | string[] };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

export const changeProjectsDisplay: ((value: IDashboardState["user"]["displayPreference"]) => IActionStructure) =
  (value: IDashboardState["user"]["displayPreference"]): IActionStructure => ({
    payload: { value },
    type: actionTypes.CHANGE_PROJECTS_DISPLAY,
  });
