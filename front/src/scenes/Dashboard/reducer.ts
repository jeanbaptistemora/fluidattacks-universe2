import _ from "lodash";
import * as actions from "./actions";
import * as vulnerabilitiesActions from "./components/Vulnerabilities/actionTypes";

export interface IDashboardState {
  vulnerabilities: {
    filters: {
      filterInputs: string;
      filterLines: string;
      filterPending: string;
      filterPorts: string;
    };
    sorts: {
      sortInputs: {};
      sortLines: {};
      sortPorts: {};
    };
  };
}

const initialState: IDashboardState = {
  vulnerabilities: {
    filters: {
      filterInputs: "",
      filterLines: "",
      filterPending: "",
      filterPorts: "",
    },
    sorts: {
      sortInputs: {},
      sortLines: {},
      sortPorts: {},
    },
  },
};

const actionMap: {
  [key: string]: ((arg1: IDashboardState, arg2: actions.IActionStructure) => IDashboardState);
} = {};

actionMap[vulnerabilitiesActions.CHANGE_FILTERS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    vulnerabilities: {
      ...state.vulnerabilities,
      filters: action.payload.filters,
    },
  });

actionMap[vulnerabilitiesActions.CHANGE_SORTS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    vulnerabilities: {
      ...state.vulnerabilities,
      sorts: action.payload.sorts,
    },
  });

type DashboardReducer = ((
  arg1: IDashboardState | undefined,
  arg2: actions.IActionStructure,
) => IDashboardState);

export const dashboard: DashboardReducer =
  (state: IDashboardState = initialState,
   action: actions.IActionStructure): IDashboardState => {
  if (action.type in actionMap) {
    return actionMap[action.type](state, action);
  } else {
    return state;
  }
};
