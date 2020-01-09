import { ThunkDispatch } from "redux-thunk";

export const CHANGE_FILTER: string = "dashboard/project/drafts/filter/change";
export interface IActionStructure {
  payload?: { [key: string]: string | string[] | {} };
  type: string;
}
export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

export const changeFilterValues: ((newValues: {}) => IActionStructure) = (newValues: {}): IActionStructure => ({
  payload: {
    filters: {...newValues},
  },
  type: CHANGE_FILTER,
});
