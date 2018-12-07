import * as actions from "./actions";
import * as actionType from "./actionTypes";
import { IEvidenceViewProps } from "./components/EvidenceView";
import { IExploitViewProps } from "./components/ExploitView";
import { ISeverityViewProps } from "./components/SeverityView";
import { IVulnerabilitiesViewProps } from "./components/Vulnerabilities/index";
import * as usersActions from "./containers/ProjectUsersView/actionTypes";
import { IProjectUsersViewProps } from "./containers/ProjectUsersView/index";
import * as recordsActions from "./containers/RecordsView/actionTypes";
import { IRecordsViewProps } from "./containers/RecordsView/index";
import * as resourcesActions from "./containers/ResourcesView/actionTypes";
import * as trackingActions from "./containers/TrackingView/actionTypes";
import { ITrackingViewProps } from "./containers/TrackingView/index";

interface IDashboardState {
  evidence: Pick<IEvidenceViewProps, "currentIndex" | "images" | "isImageOpen">;
  exploit: Pick<IExploitViewProps, "code" | "isEditing">;
  fileInput: {
    name: string;
  };
  isMdlConfirmOpen: boolean;
  records: Pick<IRecordsViewProps, "isEditing" | "dataset">;
  resources: {
    addModal: {
      envFields: Array<{ environment: string }>;
      open: boolean;
      repoFields: Array<{ branch: string; repository: string }>;
      type: "repository" | "environment" | undefined;
    };
    environments: Array<{ urlEnv: string }>;
    repositories: Array<{ branch: string; urlRepo: string }>;
  };
  severity: Pick<ISeverityViewProps, "isEditing" | "cssv2base" | "criticity" | "dataset">;
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
  };
}

const initialState: IDashboardState = {
  evidence: {
    currentIndex: 0,
    images: [],
    isImageOpen: false,
  },
  exploit: {
    code: "",
    isEditing: false,
  },
  fileInput: {
    name: "",
  },
  isMdlConfirmOpen: false,
  records: {
    dataset: [],
    isEditing: false,
  },
  resources: {
    addModal: {
      envFields: [{ environment: ""}],
      open: false,
      repoFields: [{ branch: "", repository: ""}],
      type: undefined,
    },
    environments: [],
    repositories: [],
  },
  severity: {
    criticity: 0,
    cssv2base: 0,
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

actionMap[resourcesActions.ADD_REPO_FIELD] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      addModal: {
        ...state.resources.addModal,
        repoFields: [...state.resources.addModal.repoFields, ({repository: "", branch: ""})],
      },
    },
  });

actionMap[resourcesActions.REMOVE_REPO_FIELD] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      addModal: {
        ...state.resources.addModal,
        repoFields: [...state.resources.addModal.repoFields.filter(
          (_0: { branch: string; repository: string }, index: number) => index !== action.payload.index)],
      },
    },
  });

actionMap[resourcesActions.ADD_ENV_FIELD] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      addModal: {
        ...state.resources.addModal,
        envFields: [...state.resources.addModal.envFields, ({environment: ""})],
      },
    },
  });

actionMap[resourcesActions.REMOVE_ENV_FIELD] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      addModal: {
        ...state.resources.addModal,
        envFields: [...state.resources.addModal.envFields.filter(
          (_0: { environment: string }, index: number) => index !== action.payload.index)],
      },
    },
  });

actionMap[resourcesActions.MODIFY_REPO_URL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      addModal: {
        ...state.resources.addModal,
        repoFields: [...state.resources.addModal.repoFields.map(
          (field: { branch: string; repository: string }, index: number) =>
          ({
            branch: field.branch,
            repository: index === action.payload.index
            ? action.payload.newValue
            : field.repository,
          }))],
      },
    },
  });

actionMap[resourcesActions.MODIFY_REPO_BRANCH] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      addModal: {
        ...state.resources.addModal,
        repoFields: [...state.resources.addModal.repoFields.map(
          (field: { branch: string; repository: string }, index: number) =>
          ({
            branch: index === action.payload.index
            ? action.payload.newValue
            : field.branch,
            repository: field.repository,
          }))],
      },
    },
  });

actionMap[resourcesActions.MODIFY_ENV_URL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      addModal: {
        ...state.resources.addModal,
        envFields: [...state.resources.addModal.envFields.map(
          (field: { environment: string }, index: number) =>
          ({
            environment: index === action.payload.index
            ? action.payload.newValue
            : field.environment,
          }))],
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

actionMap[actionType.LOAD_SEVERITY] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    severity: {
      ...state.severity,
      dataset: action.payload.dataset,
    },
  });

actionMap[actionType.EDIT_SEVERITY] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    severity: {
      ...state.severity,
      isEditing: !state.severity.isEditing,
    },
  });

actionMap[actionType.CALC_CVSSV2] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    severity: {
      ...state.severity,
      criticity: action.payload.temporal,
      cssv2base: action.payload.baseScore,
    },
  });

actionMap[actionType.OPEN_CONFIRM_MDL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    isMdlConfirmOpen: true,
  });

actionMap[actionType.CLOSE_CONFIRM_MDL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    isMdlConfirmOpen: false,
  });

actionMap[actionType.LOAD_EXPLOIT] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    exploit: {
      ...state.exploit,
      code: action.payload.code,
    },
  });

actionMap[actionType.EDIT_EXPLOIT] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    exploit: {
      ...state.exploit,
      isEditing: !state.exploit.isEditing,
    },
  });

actionMap[actionType.OPEN_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    evidence: {
      ...state.evidence,
      currentIndex: action.payload.imgIndex,
      isImageOpen: true,
    },
  });

actionMap[actionType.CLOSE_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    evidence: {
      ...state.evidence,
      isImageOpen: false,
    },
  });

actionMap[actionType.MOVE_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    evidence: {
      ...state.evidence,
      currentIndex: action.payload.index,
    },
  });

type DashboardReducer = ((
  arg1: IDashboardState | undefined,
  arg2: actions.IActionStructure,
) => IDashboardState);

const dashboard: DashboardReducer =
  (state: IDashboardState = initialState,
   action: actions.IActionStructure): IDashboardState => {
  if (action.type in actionMap) {
    return actionMap[action.type](state, action);
  } else {
    return state;
  }
};

export = dashboard;
