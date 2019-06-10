import { ThunkDispatch } from "redux-thunk";
import * as actionTypes from "./actionTypes";

export interface IActionStructure {
  payload?: { [key: string]: string | string[] | ({} | undefined) };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

export const openUsersMdl: ((type: "add" | "edit", initialValues?: {}) => IActionStructure) =
  (type: "add" | "edit", initialValues?: {}): IActionStructure => ({
    payload: { type, initialValues },
    type: actionTypes.OPEN_USERS_MDL,
  });

export const closeUsersMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_USERS_MDL,
  });
