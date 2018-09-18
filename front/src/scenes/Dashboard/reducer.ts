import * as actions from "./actions";
import * as actionType from "./actionTypes";

interface IDashboardState {
  resources: {
    addModal: {
      fields: Array<{ branch: string; repository: string }>;
      open: boolean;
    };
    repositories: Array<{ branch: string; repository: string }>;
  };
}

const initialState: IDashboardState = {
  resources: {
    addModal: {
      fields: [{ branch: "", repository: ""}],
      open: false,
    },
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
          },
        },
      };
    case actionType.CLOSE_ADD_MODAL:
      return {
        ...state,
        resources: {
          ...state.resources,
          addModal: {
            fields: [{ branch: "", repository: ""}],
            open: false,
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
            fields: [...state.resources.addModal.fields, ({repository: "", branch: ""})],
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
            fields: [...state.resources.addModal.fields.filter(
              (_0: { branch: string; repository: string }, index: number) => index !== action.payload.index)],
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
            fields: [...state.resources.addModal.fields.map(
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
              fields: [...state.resources.addModal.fields.map(
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
    default:
      return state;
  }
};

export = dashboard;
