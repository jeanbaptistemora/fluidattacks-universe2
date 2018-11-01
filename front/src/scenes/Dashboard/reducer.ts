import _ from "lodash";
import * as actions from "./actions";
import * as actionType from "./actionTypes";
import { IProjectUsersViewProps } from "./components/ProjectUsersView/index";
import { IVulnerabilitiesViewProps } from "./components/Vulnerabilities/index";

interface IDashboardState {
  fileInput: {
    name: string;
  };
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
  fileInput: {
    name: "",
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

type DashboardReducer = ((
  arg1: IDashboardState | undefined,
  arg2: actions.IActionStructure,
) => IDashboardState);

const actionMap: {
  [key: string]: ((arg1: IDashboardState, arg2: actions.IActionStructure) => IDashboardState);
} = {};

actionMap[actionType.LOAD_RESOURCES] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: {
      ...state.resources,
      environments: action.payload.environments,
      repositories: action.payload.repositories,
    },
  });

actionMap[actionType.CLEAR_RESOURCES] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    resources: initialState.resources,
  });

actionMap[actionType.OPEN_ADD_MODAL] =
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

actionMap[actionType.CLOSE_ADD_MODAL] =
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

actionMap[actionType.ADD_REPO_FIELD] =
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

actionMap[actionType.REMOVE_REPO_FIELD] =
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

actionMap[actionType.ADD_ENV_FIELD] =
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

actionMap[actionType.REMOVE_ENV_FIELD] =
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

actionMap[actionType.MODIFY_REPO_URL] =
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

actionMap[actionType.MODIFY_REPO_BRANCH] =
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

actionMap[actionType.MODIFY_ENV_URL] =
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

actionMap[actionType.LOAD_USERS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    users: {
      ...state.users,
      userList: action.payload.userlist,
    },
  });

actionMap[actionType.CLEAR_USERS] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    users: initialState.users,
  });

actionMap[actionType.ADD_USER] =
  (state: IDashboardState, action: actions.IActionStructure): IDashboardState =>
  ({
    ...state,
    users: {
      ...state.users,
      userList: [...state.users.userList, action.payload.newUser],
    },
  });

actionMap[actionType.REMOVE_USER] =
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

actionMap[actionType.OPEN_USERS_MDL] =
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

actionMap[actionType.CLOSE_USERS_MDL] =
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

const dashboard: DashboardReducer =
  (state: IDashboardState = initialState,
   action: actions.IActionStructure): IDashboardState => {
  if (_.has(actionMap, action.type)) {
    return actionMap[action.type](state, action);
  } else {
    return state;
  }
};

export = dashboard;
