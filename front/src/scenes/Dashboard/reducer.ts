import _ from "lodash";
import * as actions from "./actions";
import * as actionType from "./actionTypes";
import * as vulnerabilitiesActions from "./components/Vulnerabilities/actionTypes";
import { IDescriptionViewProps } from "./containers/DescriptionView";
import * as descriptionActions from "./containers/DescriptionView/actionTypes";
import * as findingActions from "./containers/FindingContent/actionTypes";
import * as homeActions from "./containers/HomeView/actionTypes";
import * as projectActions from "./containers/ProjectContent/actionTypes";
import * as findingsActions from "./containers/ProjectFindingsView/actionTypes";
import * as usersActions from "./containers/ProjectUsersView/actionTypes";
import * as recordsActions from "./containers/RecordsView/actionTypes";
import * as resourcesActions from "./containers/ResourcesView/actionTypes";
import * as severityActions from "./containers/SeverityView/actionTypes";
import { ISeverityViewProps } from "./containers/SeverityView/types";
import * as trackingActions from "./containers/TrackingView/actionTypes";
import { ITrackingViewProps } from "./containers/TrackingView/index";

export interface IDashboardState {
  confirmDialog: {[name: string]: { isOpen: boolean }};
  description: Pick<IDescriptionViewProps, "dataset" | "isEditing" | "isRemediationOpen">;
  evidence: { currentIndex: number; images: []; isEditing: boolean; isImageOpen: boolean };
  finding: {
    alert?: string;
    closedVulns: number;
    openVulns: number;
    reportDate: string;
    status: "open" | "closed" | "default";
    title: string;
  };
  findings: {
    defaultSort: {};
    filters: {
      exploitable: string;
      status: string;
      title: string;
      verification: string;
      where: string;
    };
    reportsModal: {
      isOpen: boolean;
    };
  };
  records: {
    dataset: object[];
    isEditing: boolean;
  };
  resources: {
    defaultSort: {
      environments: {};
      files: {};
      repositories: {};
      tags: {};
    };
    envModal: {
      open: boolean;
    };
    files: Array<{ description: string; fileName: string; uploadDate: string}>;
    filesModal: {
      open: boolean;
    };
    filters: {
      stateEnvironments: string;
      stateRepositories: string;
    };
    optionsModal: {
      open: boolean;
      rowInfo: { fileName: string };
    };
    reposModal: {
      open: boolean;
    };
    showUploadProgress: boolean;
    uploadProgress: number;
  };
  severity: Pick<ISeverityViewProps, "isEditing" | "severity">;
  tags: {
    tagsModal: {
      open: boolean;
    };
  };
  tracking: Pick<ITrackingViewProps, "closings">;
  updateAccessTokenModal: { open: boolean };
  user: {
    displayPreference: "grid" | "list";
    role: string;
  };
  users: {
    addModal: {
      initialValues: {};
      open: boolean;
      type: "add" | "edit";
    };
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
  confirmDialog: {},
  description: {
    dataset: {
      acceptanceDate: "",
      acceptationApproval: "",
      acceptationJustification: "",
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
  finding: {
    alert: undefined,
    closedVulns: 0,
    openVulns: 0,
    reportDate: "-",
    status: "default",
    title: "",
  },
  findings: {
    defaultSort: {},
    filters: {
      exploitable: "",
      status: "",
      title: "",
      verification: "",
      where: "",
    },
    reportsModal: {
      isOpen: false,
    },
  },
  records: {
    dataset: [],
    isEditing: false,
  },
  resources: {
    defaultSort: {
      environments: {},
      files: {},
      repositories: {},
      tags: {},
    },
    envModal: {
      open: false,
    },
    files: [],
    filesModal: {
      open: false,
    },
    filters: {
      stateEnvironments: "",
      stateRepositories: "",
    },
    optionsModal: {
      open: false,
      rowInfo: {fileName: ""},
    },
    reposModal: {
      open: false,
    },
    showUploadProgress: false,
    uploadProgress: 0,
  },
  severity: {
    isEditing: false,
    severity: 0,
  },
  tags: {
    tagsModal: {
      open: false,
    },
  },
  tracking: {
    closings: [],
  },
  updateAccessTokenModal: { open: false },
  user: {
    displayPreference: _.get(localStorage, "projectsDisplay", "grid"),
    role: "",
  },
  users: {
    addModal: {
      initialValues: {},
      open: false,
      type: "add",
    },
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

actionMap[resourcesActions.CHANGE_FILTERS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      filters: action.payload.filters,
    },
  });

actionMap[resourcesActions.CHANGE_SORTED] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      defaultSort: action.payload.defaultSort,
    },
  });

actionMap[resourcesActions.LOAD_RESOURCES] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      files: action.payload.files,
    },
  });

actionMap[resourcesActions.OPEN_ENVIRONMENTS_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      envModal: {
        ...state.resources.envModal,
        open: true,
      },
    },
  });

actionMap[resourcesActions.CLOSE_ENVIRONMENTS_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      envModal: {
        ...initialState.resources.envModal,
      },
    },
  });

actionMap[resourcesActions.OPEN_REPOSITORIES_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      reposModal: {
        ...state.resources.reposModal,
        open: true,
      },
    },
  });

actionMap[resourcesActions.CLOSE_REPOSITORIES_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      reposModal: {
        ...initialState.resources.reposModal,
      },
    },
  });

actionMap[resourcesActions.OPEN_FILES_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      filesModal: {
        ...state.resources.filesModal,
        open: true,
      },
    },
  });

actionMap[resourcesActions.CLOSE_FILES_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      filesModal: {
        ...initialState.resources.filesModal,
      },
    },
  });

actionMap[resourcesActions.OPEN_OPTIONS_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      optionsModal: {
        ...state.resources.optionsModal,
        open: true,
        rowInfo: action.payload.rowInfo,
      },
    },
  });

actionMap[resourcesActions.CLOSE_OPTIONS_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      optionsModal: {
        ...initialState.resources.optionsModal,
      },
    },
  });

actionMap[resourcesActions.OPEN_TAGS_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    tags: {
      ...state.tags,
      tagsModal: {
        ...state.tags.tagsModal,
        open: true,
      },
    },
  });

actionMap[resourcesActions.CLOSE_TAGS_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    tags: {
      ...state.tags,
      tagsModal: initialState.tags.tagsModal,
    },
  });

actionMap[resourcesActions.UPDATE_UPLOAD_PROGRESS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      uploadProgress: action.payload.percentCompleted,
    },
  });

actionMap[resourcesActions.SHOW_UPLOAD_PROGRESS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      showUploadProgress: !state.resources.showUploadProgress,
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

actionMap[severityActions.EDIT_SEVERITY] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    severity: {
      ...state.severity,
      isEditing: !state.severity.isEditing,
    },
  });

actionMap[severityActions.CALC_CVSS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    severity: {
      ...state.severity,
      severity: action.payload.temporal,
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

actionMap[actionType.OPEN_ACCESS_TOKEN_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
    ({
      ...state,
      updateAccessTokenModal: {
        ...state.updateAccessTokenModal,
        open: true,
      },
  });

actionMap[actionType.CLOSE_ACCESS_TOKEN_MODAL] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
    ({
      ...state,
      updateAccessTokenModal: {
        ...state.updateAccessTokenModal,
        open: false,
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

actionMap[descriptionActions.CLEAR_EVIDENCE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
    ({
      ...state,
      description: initialState.description,
    });

actionMap[findingActions.LOAD_FINDING] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
    ({
      ...state,
      finding: action.payload,
    });

actionMap[findingActions.CLEAR_FINDING_STATE] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
    ({
      ...state,
      description: initialState.description,
      evidence: initialState.evidence,
      finding: initialState.finding,
      records: initialState.records,
      severity: initialState.severity,
      tracking: initialState.tracking,
    });

actionMap[findingActions.UPDATE_FINDING_HEADER] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState => ({
    ...state,
    finding: { ...state.finding, ...action.payload },
  });

actionMap[projectActions.LOAD_PROJECT] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState => ({
    ...state,
    user: {
      ...state.user,
      role: action.payload.role,
    },
  });

actionMap[projectActions.CLEAR_PROJECT_STATE] = (state: IDashboardState): IDashboardState => ({
  ...state,
  findings: {
    ...initialState.findings,
    defaultSort: state.findings.defaultSort,
    filters: {
      ...state.findings.filters,
    },
  },
  resources: {
    ...initialState.resources,
    defaultSort: {
      ...state.resources.defaultSort,
    },
    filters: {
      ...state.resources.filters,
    },
  },
  users: initialState.users,
});

actionMap[findingsActions.OPEN_REPORTS_MODAL] = (state: IDashboardState): IDashboardState => ({
  ...state,
  findings: {
    ...state.findings,
    reportsModal: {
      isOpen: true,
    },
  },
});

actionMap[findingsActions.CHANGE_FILTER] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState => ({
    ...state,
    findings: {
      ...state.findings,
      filters: action.payload.filters,
    },
  });

actionMap[findingsActions.CHANGE_SORTED] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState => ({
      ...state,
      findings: {
        ...state.findings,
        defaultSort: action.payload.defaultSort,
      },
    });

actionMap[findingsActions.CLOSE_REPORTS_MODAL] = (state: IDashboardState): IDashboardState => ({
  ...state,
  findings: {
    ...state.findings,
    reportsModal: {
      isOpen: false,
    },
  },
});

actionMap[homeActions.CHANGE_PROJECTS_DISPLAY] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState => ({
    ...state,
    user: {
      ...state.user,
      displayPreference: action.payload.value,
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
