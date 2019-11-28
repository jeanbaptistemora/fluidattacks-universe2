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
