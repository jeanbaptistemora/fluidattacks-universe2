/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkDispatch } from "redux-thunk";
import * as actionType from "./actionTypes";

export interface IActionStructure {
  payload?: any;
  type: string;
}

export type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;

export const openConfirmDialog: ((dialogName: string) => IActionStructure) =
  (dialogName: string): IActionStructure => ({
    payload: { dialogName },
    type: actionType.OPEN_CONFIRM_DIALOG,
  });

export const closeConfirmDialog: ((dialogName: string) => IActionStructure) =
  (dialogName: string): IActionStructure => ({
    payload: { dialogName },
    type: actionType.CLOSE_CONFIRM_DIALOG,
  });

export const closeAddUserModal: (() => IActionStructure) =
  (): IActionStructure => ({
    type: actionType.CLOSE_ADD_USER_MODAL,
  });

export const closeUpdateAccessToken: (() => IActionStructure) =
  (): IActionStructure => ({
    type: actionType.CLOSE_ACCESS_TOKEN_MODAL,
  });

export const openAddUserModal: (() => IActionStructure) =
  (): IActionStructure => ({
    type: actionType.OPEN_ADD_USER_MODAL,
  });

export const openUpdateAccessToken: (() => IActionStructure) =
  (): IActionStructure => ({
    type: actionType.OPEN_ACCESS_TOKEN_MODAL,
  });
