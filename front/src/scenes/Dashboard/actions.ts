/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */

export interface IActionStructure {
  payload?: any;
  type: string;
}
