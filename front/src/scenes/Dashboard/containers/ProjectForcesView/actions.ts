export const CHANGE_SORTS: string = "dashboard/project/events/sort/change";

export interface IActionStructure {
  payload?: { [key: string]: string | string[] | {} };
  type: string;
}

export const changeSortValues: ((newValues: {}) => IActionStructure) =
(newValues: {}): IActionStructure => ({
  payload: {
    defaultSort: newValues,
  },
  type: CHANGE_SORTS,
});
