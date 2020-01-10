import { ThunkDispatch } from "redux-thunk";

export const CHANGE_FILTER: string = "dashboard/project/drafts/filter/change";
export const CHANGE_SORTS: string = "dashboard/project/drafts/sort/change";
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

export const changeSortValues: ((newValues: {}) => IActionStructure) = (newValues: {}): IActionStructure => ({
  payload: {
    defaultSort: newValues,
  },
  type: CHANGE_SORTS,
});
