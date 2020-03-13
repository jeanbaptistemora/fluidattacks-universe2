import _ from "lodash";
import * as actions from "./actions";
import * as vulnerabilitiesActions from "./components/Vulnerabilities/actionTypes";
import { IDescriptionViewProps } from "./containers/DescriptionView";
import * as descriptionActions from "./containers/DescriptionView/actionTypes";
import * as projectActions from "./containers/ProjectContent/actionTypes";

export interface IDashboardState {
  description: Pick<IDescriptionViewProps, "dataset" | "isEditing" | "isRemediationOpen">;
  updateAccessTokenModal: { open: boolean };
  user: {
    role: string;
  };
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
  description: {
    dataset: {
      acceptanceDate: "",
      acceptationApproval: "",
      acceptationUser: "",
      actor: "",
      affectedSystems: "",
      analyst: "",
      attackVectorDesc: "",
      btsUrl: "",
      clientCode: "",
      clientProject: "",
      compromisedAttributes: "",
      compromisedRecords: "",
      cweUrl: "",
      description: "",
      historicTreatment: [{date: "", treatment: "", user: ""}],
      justification: "",
      newRemediated: false,
      openVulnerabilities: "",
      recommendation: "",
      releaseDate: "",
      remediated: false,
      requirements: "",
      risk: "",
      scenario: "",
      state: "",
      subscription: "",
      threat: "",
      title: "",
      treatment: "",
      treatmentManager: "",
      type: "",
      userEmails: [{ email: "" }],
      verified: false,
    },
    isEditing: false,
    isRemediationOpen : false,
  },
  updateAccessTokenModal: { open: false },
  user: {
    role: "",
  },
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

actionMap[descriptionActions.LOAD_DESCRIPTION] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    description: {
      ...state.description,
      dataset: {...state.description.dataset, ...action.payload.descriptionData},
    },
  });

actionMap[descriptionActions.EDIT_DESCRIPTION] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    description: {
      ...state.description,
      isEditing: !state.description.isEditing,
    },
  });

actionMap[descriptionActions.OPEN_REMEDIATION_MDL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState => ({
    ...state,
    description: {
      ...state.description,
      isRemediationOpen: true,
    },
  });

actionMap[descriptionActions.CLOSE_REMEDIATION_MDL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState => ({
    ...state,
    description: {
      ...state.description,
      isRemediationOpen: false,
    },
  });

actionMap[descriptionActions.CLEAR_DESCRIPTION] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
    ({
      ...state,
      description: initialState.description,
    });

actionMap[projectActions.LOAD_PROJECT] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState => ({
    ...state,
    user: {
      ...state.user,
      role: action.payload.role,
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
