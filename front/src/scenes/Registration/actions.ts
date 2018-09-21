/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import * as actionType from "./actionTypes";

export interface IActionStructure {
  payload: any;
  type: string;
}

type RegistrationAction = ((...args: any[]) => IActionStructure);

export const checkRemember: RegistrationAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.CHECK_REMEMBER,
});
