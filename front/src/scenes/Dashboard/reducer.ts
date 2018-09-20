import * as actions from "./actions";
import * as actionType from "./actionTypes";

interface IDashboardState {
  resources: {
    addModal: {
      envFields: Array<{ environment: string }>;
      open: boolean;
      repoFields: Array<{ branch: string; repository: string }>;
      type: "repository" | "environment" | undefined;
    };
    environments: Array<{ environment: string }>;
    repositories: Array<{ branch: string; repository: string }>;
  };
}

const initialState: IDashboardState = {
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
};

type DashboardReducer = ((
  arg1: IDashboardState | undefined,
  arg2: actions.IActionStructure,
) => IDashboardState);

const dashboard: DashboardReducer =
  (state: IDashboardState = initialState,
   action: actions.IActionStructure): IDashboardState => {
  switch (action.type) {
    case actionType.LOAD_RESOURCES:
      return {
        ...state,
        resources: {
          ...state.resources,
          environments: action.payload.environments,
          repositories: action.payload.repositories,
        },
      };
    case actionType.OPEN_ADD_MODAL:
      return {
        ...state,
        resources: {
          ...state.resources,
          addModal: {
            ...state.resources.addModal,
            open: true,
            type: action.payload.type,
          },
        },
      };
    case actionType.CLOSE_ADD_MODAL:
      return {
        ...state,
        resources: {
          ...state.resources,
          addModal: {
            ...initialState.resources.addModal,
          },
        },
      };
    case actionType.ADD_REPO_FIELD:
      return {
        ...state,
        resources: {
          ...state.resources,
          addModal: {
            ...state.resources.addModal,
            repoFields: [...state.resources.addModal.repoFields, ({repository: "", branch: ""})],
          },
        },
      };
    case actionType.REMOVE_REPO_FIELD:
      return {
        ...state,
        resources: {
          ...state.resources,
          addModal: {
            ...state.resources.addModal,
            repoFields: [...state.resources.addModal.repoFields.filter(
              (_0: { branch: string; repository: string }, index: number) => index !== action.payload.index)],
          },
        },
      };
    case actionType.ADD_ENV_FIELD:
      return {
        ...state,
        resources: {
          ...state.resources,
          addModal: {
            ...state.resources.addModal,
            envFields: [...state.resources.addModal.envFields, ({environment: ""})],
          },
        },
      };
    case actionType.REMOVE_ENV_FIELD:
      return {
        ...state,
        resources: {
          ...state.resources,
          addModal: {
            ...state.resources.addModal,
            envFields: [...state.resources.addModal.envFields.filter(
              (_0: { environment: string }, index: number) => index !== action.payload.index)],
          },
        },
      };
    case actionType.MODIFY_REPO_URL:
      return {
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
      };
      case actionType.MODIFY_REPO_BRANCH:
        return {
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
        };
    case actionType.MODIFY_ENV_URL:
      return {
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
      };
    default:
      return state;
  }
};

export = dashboard;
