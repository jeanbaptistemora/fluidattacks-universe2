import { ThunkDispatch } from "redux-thunk";
import * as actionTypes from "./actionTypes";

export interface IActionStructure {
  payload?: { [key: string]: string | string[] };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

export const clearFindingState: (() => IActionStructure) = (): IActionStructure => ({
  type: actionTypes.CLEAR_FINDING_STATE,
});
