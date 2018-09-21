/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import * as actionType from "./actionTypes";

export interface IActionStructure {
  payload: any;
  type: string;
}

type DashboardAction = ((...args: any[]) => IActionStructure);

export const loadResources: DashboardAction =
  (repos: string[], envs: string[]): IActionStructure => ({
    payload: {
      environments: envs,
      repositories: repos,
    },
    type: actionType.LOAD_RESOURCES,
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
