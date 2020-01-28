/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import * as actionType from "./actionTypes";

export interface IActionStructure {
  payload?: any;
  type: string;
}

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
