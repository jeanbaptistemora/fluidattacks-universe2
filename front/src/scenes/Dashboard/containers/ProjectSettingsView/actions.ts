import { ThunkDispatch } from "redux-thunk";
import * as actionTypes from "./actionTypes";

export interface IActionStructure {
  payload?: { [key: string]: string | number | string[] | ({} | undefined) };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

export const changeSortedValues: ((newValues: {}) => IActionStructure) = (newValues: {}): IActionStructure => ({
    payload: {
      defaultSort: {
        ...newValues,
      },
    },
    type: actionTypes.CHANGE_SORTED,
  });

export const openTagsModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_TAGS_MODAL,
  });

export const closeTagsModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_TAGS_MODAL,
  });
