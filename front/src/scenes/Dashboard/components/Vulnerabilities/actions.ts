import { IActionStructure } from "../../actions";
import * as actionTypes from "./actionTypes";

export const changeFilterValues: ((newValues: {}) => IActionStructure) = (newValues: {}): IActionStructure => ({
  payload: {
    filters: {
      ...newValues,
    },
  },
  type: actionTypes.CHANGE_FILTERS,
});

export const changeSortValues: ((newValues: {}) => IActionStructure) = (newValues: {}): IActionStructure => ({
    payload: {
      sorts: {
        ...newValues,
      },
    },
    type: actionTypes.CHANGE_SORTS,
  });
