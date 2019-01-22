import { Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import * as actionTypes from "./actionTypes";
export interface IActionStructure {
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the payload
   * type may differ between actions
   */
  payload: any;
  type: string;
}

type ThunkDispatcher = Dispatch<IActionStructure> & ThunkDispatch<{}, {}, IActionStructure>;
/* tslint:disable-next-line:no-any
 * Disabling this rule is necessary because the args
 * of an async action may differ
 */
type ThunkActionStructure<T> = ((...args: any[]) => ThunkAction<T, {}, {}, IActionStructure>);

export const editDescription: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.EDIT_DESCRIPTION,
  });

export const openRemediationMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_REMEDIATION_MDL,
  });

export const closeRemediationMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_REMEDIATION_MDL,
  });

export const openConfirmMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_CONFIRM_MDL,
  });

export const closeConfirmMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_CONFIRM_MDL,
  });

