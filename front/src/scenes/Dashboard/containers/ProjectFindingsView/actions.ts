import { ThunkDispatch } from "redux-thunk";
import * as actionTypes from "./actionTypes";

export interface IActionStructure {
  payload?: { [key: string]: string | string[] | {} };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

export const openReportsModal: (() => IActionStructure) = (): IActionStructure => ({
  type: actionTypes.OPEN_REPORTS_MODAL,
});

export const closeReportsModal: (() => IActionStructure) = (): IActionStructure => ({
  type: actionTypes.CLOSE_REPORTS_MODAL,
});

export const changeSortedValues: ((newValues: {}) => IActionStructure) = (newValues: {}): IActionStructure => ({
  payload: {
    defaultSort: newValues,
  },
  type: actionTypes.CHANGE_SORTED,
});
