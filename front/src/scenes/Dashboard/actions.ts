/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../utils/notifications";
import rollbar from "../../utils/rollbar";
import Xhr from "../../utils/xhr";
import * as actionType from "./actionTypes";
import { IProjectUsersViewProps } from "./components/ProjectUsersView/index";
import { IRecordsViewProps } from "./components/RecordsView";
import { IVulnerabilitiesViewProps } from "./components/Vulnerabilities/index";

export interface IActionStructure {
  payload: any;
  type: string;
}

type DashboardAction = ((...args: any[]) => IActionStructure);
type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, AnyAction>);

export const loadResources: DashboardAction =
  (repos: Array<{ branch: string; urlRepo: string }>,
   envs: Array<{ urlEnv: string }>): IActionStructure => ({
    payload: {
      environments: envs,
      repositories: repos,
    },
    type: actionType.LOAD_RESOURCES,
});

export const clearResources: DashboardAction =
  (): IActionStructure => ({
  payload: undefined,
  type: actionType.CLEAR_RESOURCES,
});

export const addRepositoryField: DashboardAction =
  (): IActionStructure => ({
      payload: undefined,
      type: actionType.ADD_REPO_FIELD,
});

export const removeRepositoryField: DashboardAction =
  (index: number): IActionStructure => ({
      payload: { index },
      type: actionType.REMOVE_REPO_FIELD,
});

export const addEnvironmentField: DashboardAction =
  (): IActionStructure => ({
      payload: undefined,
      type: actionType.ADD_ENV_FIELD,
});

export const removeEnvironmentField: DashboardAction =
  (index: number): IActionStructure => ({
      payload: { index },
      type: actionType.REMOVE_ENV_FIELD,
});

export const openAddModal: DashboardAction =
  (type: "repository" | "environment"): IActionStructure => ({
      payload: { type },
      type: actionType.OPEN_ADD_MODAL,
});

export const closeAddModal: DashboardAction =
  (): IActionStructure => ({
      payload: undefined,
      type: actionType.CLOSE_ADD_MODAL,
});

export const modifyRepoUrl: DashboardAction =
  (index: number, newValue: string): IActionStructure => ({
      payload: {
        index,
        newValue,
      },
      type: actionType.MODIFY_REPO_URL,
});

export const modifyRepoBranch: DashboardAction =
  (index: number, newValue: string): IActionStructure => ({
      payload: {
        index,
        newValue,
      },
      type: actionType.MODIFY_REPO_BRANCH,
});

export const modifyEnvUrl: DashboardAction =
  (index: number, newValue: string): IActionStructure => ({
      payload: {
        index,
        newValue,
      },
      type: actionType.MODIFY_ENV_URL,
});

export const addFileName: DashboardAction =
  (newValue: string): IActionStructure => ({
      payload: {
        newValue,
      },
      type: actionType.ADD_FILE_NAME,
});

export const loadUsers: DashboardAction =
  (userlist: IProjectUsersViewProps["userList"]): IActionStructure => ({
    payload: {
      userlist,
    },
    type: actionType.LOAD_USERS,
});

export const clearUsers: DashboardAction =
  (): IActionStructure => ({
  payload: undefined,
  type: actionType.CLEAR_USERS,
});

export const addUser: DashboardAction =
  (newUser: IProjectUsersViewProps["userList"][0]): IActionStructure => ({
    payload: { newUser },
    type: actionType.ADD_USER,
});

export const removeUser: DashboardAction =
  (removedEmail: string): IActionStructure => ({
    payload: { removedEmail },
    type: actionType.REMOVE_USER,
});

export const openUsersMdl: DashboardAction =
  (type: "add" | "edit", initialValues?: {}): IActionStructure => ({
    payload: { type, initialValues },
    type: actionType.OPEN_USERS_MDL,
});

export const closeUsersMdl: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.CLOSE_USERS_MDL,
});
export const loadVulnerabilities: DashboardAction =
  (dataInputs: IVulnerabilitiesViewProps["dataInputs"],
   dataLines: IVulnerabilitiesViewProps["dataLines"],
   dataPorts: IVulnerabilitiesViewProps["dataPorts"]): IActionStructure => ({
    payload: {
      dataInputs,
      dataLines,
      dataPorts,
    },
    type: actionType.LOAD_VULNERABILITIES,
});

export const loadRecords: ThunkActionStructure =
(
  findingId: IRecordsViewProps["findingId"],
): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
  let gQry: string;
  gQry = `{
    finding(identifier: "${findingId}") {
      records
    }
  }`;
  new Xhr().request(gQry, "An error occurred getting compromised records")
  .then((response: AxiosResponse) => {
    const { data } = response.data;
    dispatch({
      payload: { records: JSON.parse(data.finding.records) },
      type: actionType.LOAD_RECORDS,
    });
  })
  .catch((error: AxiosError) => {
    if (error.response !== undefined) {
      const { errors } = error.response.data;

      msgError("There was an error :(");
      rollbar.error(error.message, errors);
    }
  });
};

export const editRecords: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.EDIT_RECORDS,
});
