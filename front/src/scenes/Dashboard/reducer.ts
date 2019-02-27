import * as actions from "./actions";
import * as actionType from "./actionTypes";
import { IVulnerabilitiesViewProps } from "./components/Vulnerabilities/index";
import { IDescriptionViewProps } from "./containers/DescriptionView";
import * as descriptionActions from "./containers/DescriptionView/actionTypes";
import { IEvidenceViewProps } from "./containers/EvidenceView";
import * as evidenceActions from "./containers/EvidenceView/actionTypes";
import { IExploitViewProps } from "./containers/ExploitView";
import * as exploitActions from "./containers/ExploitView/actionTypes";
import * as indicatorsActions from "./containers/IndicatorsView/actionTypes";
import * as usersActions from "./containers/ProjectUsersView/actionTypes";
import { IProjectUsersViewProps } from "./containers/ProjectUsersView/index";
import * as recordsActions from "./containers/RecordsView/actionTypes";
import { IRecordsViewProps } from "./containers/RecordsView/index";
import * as resourcesActions from "./containers/ResourcesView/actionTypes";
import { ISeverityViewProps } from "./containers/SeverityView";
import * as severityActions from "./containers/SeverityView/actionTypes";
import * as trackingActions from "./containers/TrackingView/actionTypes";
import { ITrackingViewProps } from "./containers/TrackingView/index";

export interface IDashboardState {
  confirmDialog: {[name: string]: { isOpen: boolean }};
  description: Pick<IDescriptionViewProps, "dataset" | "isEditing" | "isRemediationOpen">;
  evidence: Pick<IEvidenceViewProps, "currentIndex" | "images" | "isImageOpen" | "isEditing">;
  exploit: Pick<IExploitViewProps, "code" | "isEditing">;
  fileInput: {
    name: string;
  };
  indicators: {
    addModal: {
      open: boolean;
    };
    deletionDate: string;
    subscription: string;
    tags: string[];
  };
  records: Pick<IRecordsViewProps, "isEditing" | "dataset">;
  resources: {
    addModal: {
      open: boolean;
      type: "repository" | "environment" | undefined;
    };
    environments: Array<{ urlEnv: string }>;
    files: Array<{ description: string; fileName: string; uploadDate: string}>;
    repositories: Array<{ branch: string; urlRepo: string }>;
  };
  severity: Pick<ISeverityViewProps, "isEditing" | "criticity" | "dataset">;
  tracking: Pick<ITrackingViewProps, "closings">;
  users: {
    addModal: {
      initialValues: {};
      open: boolean;
      type: "add" | "edit" | undefined;
    };
    userList: IProjectUsersViewProps["userList"];
  };
  vulnerabilities: {
    dataInputs: IVulnerabilitiesViewProps["dataInputs"];
    dataLines: IVulnerabilitiesViewProps["dataLines"];
    dataPorts: IVulnerabilitiesViewProps["dataPorts"];
    releaseDate: IVulnerabilitiesViewProps["releaseDate"];
  };
}

const initialState: IDashboardState = {
  confirmDialog: {},
  description: {
    dataset: {
      actor: "",
      affectedSystems: "",
      ambit: "",
      attackVector: "",
      btsUrl: "",
      category: "",
      clientCode: "",
      clientProject: "",
      compromisedAttributes: "",
      compromisedRecords: "",
      cweUrl: "",
      description: "",
      detailedSeverity: 0,
      kbUrl: "",
      probability: 0,
      recommendation: "",
      releaseDate: "",
      remediated: false,
      reportLevel: "",
      requirements: "",
      risk: "",
      riskLevel: "",
      scenario: "",
      state: "",
      subscription: "",
      threat: "",
      title: "",
      treatment: "",
      treatmentJustification: "",
      treatmentManager: "",
      type: "",
      userEmails: [{ email: "" }],
    },
    isEditing: false,
    isRemediationOpen : false,
  },
  evidence: {
    currentIndex: 0,
    images: [],
    isEditing: false,
    isImageOpen: false,
  },
  exploit: {
    code: "",
    isEditing: false,
  },
  fileInput: {
    name: "",
  },
  indicators: {
    addModal: {
      open: false,
    },
    deletionDate: "",
    subscription: "",
    tags: [],
  },
  records: {
    dataset: [],
    isEditing: false,
  },
  resources: {
    addModal: {
      open: false,
      type: undefined,
    },
    environments: [],
    files: [],
    repositories: [],
  },
  severity: {
    criticity: 0,
    dataset: {
      accessComplexity: "",
      accessVector: "",
      authentication: "",
      availabilityImpact: "",
      availabilityRequirement: "",
      collateralDamagePotential: "",
      confidenceLevel: "",
      confidentialityImpact: "",
      confidentialityRequirement: "",
      exploitability: "",
      findingDistribution: "",
      integrityImpact: "",
      integrityRequirement: "",
      resolutionLevel: "",
    },
    isEditing: false,
  },
  tracking: {
    closings: [],
  },
  users: {
    addModal: {
      initialValues: {},
      open: false,
      type: undefined,
    },
    userList: [],
  },
  vulnerabilities: {
    dataInputs: [],
    dataLines: [],
    dataPorts: [],
    releaseDate: "",
  },
};

const actionMap: {
  [key: string]: ((arg1: IDashboardState, arg2: actions.IActionStructure) => IDashboardState);
} = {};

actionMap[resourcesActions.LOAD_RESOURCES] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      environments: action.payload.environments,
      files: action.payload.files,
      repositories: action.payload.repositories,
    },
  });

actionMap[resourcesActions.CLEAR_RESOURCES] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: initialState.resources,
  });

actionMap[resourcesActions.OPEN_ADD_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      addModal: {
        ...state.resources.addModal,
        open: true,
        type: action.payload.type,
      },
    },
  });

actionMap[resourcesActions.CLOSE_ADD_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      addModal: {
        ...initialState.resources.addModal,
      },
    },
  });

actionMap[actionType.ADD_FILE_NAME] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    fileInput: {
      name: action.payload.newValue[0].name,
    },
  });

actionMap[usersActions.LOAD_USERS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    users: {
      ...state.users,
      userList: action.payload.userlist,
    },
  });

actionMap[usersActions.CLEAR_USERS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    users: initialState.users,
  });

actionMap[usersActions.ADD_USER] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    users: {
      ...state.users,
      userList: [...state.users.userList, action.payload.newUser],
    },
  });

actionMap[usersActions.REMOVE_USER] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    users: {
      ...state.users,
      userList: [...state.users.userList.filter(
        (user: IProjectUsersViewProps["userList"][0]) =>
        user.email !== action.payload.removedEmail,
      )],
    },
  });

actionMap[usersActions.OPEN_USERS_MDL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    users: {
      ...state.users,
      addModal: {
        ...state.users.addModal,
        initialValues: action.payload.initialValues,
        open: true,
        type: action.payload.type,
      },
    },
  });

actionMap[usersActions.CLOSE_USERS_MDL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    users: {
      ...state.users,
      addModal: initialState.users.addModal,
    },
  });

actionMap[actionType.LOAD_VULNERABILITIES] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    vulnerabilities: {
      dataInputs: action.payload.dataInputs,
      dataLines: action.payload.dataLines,
      dataPorts: action.payload.dataPorts,
      releaseDate: action.payload.releaseDate,
    },
  });

actionMap[recordsActions.EDIT_RECORDS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    records: {
      ...state.records,
      isEditing: !state.records.isEditing,
    },
  });

actionMap[recordsActions.LOAD_RECORDS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    records: {
      ...state.records,
      dataset: action.payload.records,
    },
  });

actionMap[trackingActions.LOAD_TRACKING] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    tracking: {
      closings: action.payload.closings,
    },
  });

actionMap[severityActions.LOAD_SEVERITY] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    severity: {
      ...state.severity,
      dataset: action.payload.dataset,
    },
  });

actionMap[severityActions.EDIT_SEVERITY] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    severity: {
      ...state.severity,
      isEditing: !state.severity.isEditing,
    },
  });

actionMap[severityActions.CALC_CVSSV2] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    severity: {
      ...state.severity,
      criticity: action.payload.temporal,
    },
  });

actionMap[actionType.OPEN_CONFIRM_DIALOG] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
    ({
      ...state,
      confirmDialog: {
        ...state.confirmDialog,
        [action.payload.dialogName]: {
          ...state.confirmDialog[action.payload.dialogName],
          isOpen: true,
        },
      },
    });

actionMap[actionType.CLOSE_CONFIRM_DIALOG] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
    ({
      ...state,
      confirmDialog: {
        ...state.confirmDialog,
        [action.payload.dialogName]: {
          ...state.confirmDialog[action.payload.dialogName],
          isOpen: false,
        },
      },
    });

actionMap[exploitActions.LOAD_EXPLOIT] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    exploit: {
      ...state.exploit,
      code: action.payload.code,
    },
  });

actionMap[exploitActions.EDIT_EXPLOIT] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    exploit: {
      ...state.exploit,
      isEditing: !state.exploit.isEditing,
    },
  });

actionMap[evidenceActions.OPEN_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    evidence: {
      ...state.evidence,
      currentIndex: action.payload.imgIndex,
      isImageOpen: true,
    },
  });

actionMap[evidenceActions.CLOSE_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    evidence: {
      ...state.evidence,
      isImageOpen: false,
    },
  });

actionMap[evidenceActions.MOVE_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    evidence: {
      ...state.evidence,
      currentIndex: action.payload.index,
    },
  });

actionMap[evidenceActions.EDIT_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    evidence: {
      ...state.evidence,
      isEditing: action.payload.value,
    },
  });

actionMap[evidenceActions.LOAD_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    evidence: {
      ...state.evidence,
      images: action.payload.images,
    },
  });

actionMap[evidenceActions.CLEAR_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    evidence: initialState.evidence,
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
actionMap[indicatorsActions.LOAD_TAGS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    indicators: {
      ...state.indicators,
      deletionDate: action.payload.deletionDate,
      subscription: action.payload.subscription,
      tags: action.payload.tags,
    },
  });

actionMap[indicatorsActions.CLEAR_TAGS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    indicators: initialState.indicators,
  });

actionMap[indicatorsActions.OPEN_ADD_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    indicators: {
      ...state.indicators,
      addModal: {
        ...state.indicators.addModal,
        open: true,
      },
    },
  });
actionMap[indicatorsActions.CLOSE_ADD_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    indicators: {
      ...state.indicators,
      addModal: {
        ...initialState.indicators.addModal,
      },
    },
  });

actionMap[descriptionActions.CLEAR_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
    ({
      ...state,
      description: initialState.description,
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
