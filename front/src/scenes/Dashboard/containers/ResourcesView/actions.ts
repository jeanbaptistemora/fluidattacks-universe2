import { AxiosError, AxiosResponse } from "axios";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import { IDashboardState } from "../../reducer";
import * as actionTypes from "./actionTypes";

type IResources = IDashboardState["resources"];

export interface IActionStructure {
  payload?: { [key: string]: string | number | string[] | ({} | undefined) };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

type ThunkResult<T> = ThunkAction<T, {}, undefined, IActionStructure>;

export const loadResources: ((projectName: string) => ThunkResult<void>) =
  (projectName: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `{
        resources (projectName: "${projectName}") {
          environments
          repositories
          files
        }
    }`;
      new Xhr().request(gQry, "An error occurred getting repositories")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          dispatch({
            payload: {
              environments: JSON.parse(data.resources.environments),
              files: JSON.parse(data.resources.files),
              repositories: JSON.parse(data.resources.repositories),
            },
            type: actionTypes.LOAD_RESOURCES,
          });
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;

            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error(error.message, errors);
          }
        });
    };

export const openAddEnvModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_ENVIRONMENTS_MODAL,
  });

export const closeAddEnvModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_ENVIRONMENTS_MODAL,
  });

export const openAddRepoModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_REPOSITORIES_MODAL,
  });

export const closeAddRepoModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_REPOSITORIES_MODAL,
  });

export const openAddFilesModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_FILES_MODAL,
  });

export const closeAddFilesModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_FILES_MODAL,
  });

export const openOptionsModal: ((rowInfo: string | undefined) => IActionStructure) =
  (rowInfo: string | undefined): IActionStructure => ({
    payload: {rowInfo},
    type: actionTypes.OPEN_OPTIONS_MODAL,
  });

export const closeOptionsModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_OPTIONS_MODAL,
  });

export const saveRepos: ((projectName: string, reposData: IResources["repositories"]) => ThunkResult<void>) =
  (projectName: string, reposData: IResources["repositories"],
): ThunkResult<void> => (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
        addRepositories (
          resourcesData: ${JSON.stringify(JSON.stringify(reposData))},
          projectName: "${projectName}") {
          success
          resources {
            environments
            files
            repositories
          }
        }
      }`;
    new Xhr().request(gQry, "An error occurred adding repositories")
      .then((response: AxiosResponse) => {
        const { data } = response.data;
        if (data.addRepositories.success) {
          dispatch(closeAddRepoModal());
          dispatch({
            payload: {
              environments: JSON.parse(data.addRepositories.resources.environments),
              files: JSON.parse(data.addRepositories.resources.files),
              repositories: JSON.parse(data.addRepositories.resources.repositories),
            },
            type: actionTypes.LOAD_RESOURCES,
          });
          msgSuccess(
            translate.t("search_findings.tab_resources.success"),
            translate.t("search_findings.tab_users.title_success"),
          );
        } else {
          msgError(translate.t("proj_alerts.error_textsad"));
          rollbar.error("An error occurred adding repositories");
        }
      })
      .catch((error: AxiosError) => {
        if (error.response !== undefined) {
          const { errors } = error.response.data;

          msgError(translate.t("proj_alerts.error_textsad"));
          rollbar.error(error.message, errors);
        }
      });
  };

export const removeRepo: ((projectName: string, reposData: {[value: string]: string | null}) => ThunkResult<void>) =
  (projectName: string, reposData: {[value: string]: string | null}): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
      removeRepositories (
        repositoryData: ${JSON.stringify(JSON.stringify(reposData))},
        projectName: "${projectName}"
      ) {
        success
        resources {
          environments
          repositories
          files
        }
      }
    }`;
      new Xhr().request(gQry, "An error occurred removing repositories")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.removeRepositories.success) {
            dispatch({
              payload: {
                environments: JSON.parse(data.removeRepositories.resources.environments),
                files: JSON.parse(data.removeRepositories.resources.files),
                repositories: JSON.parse(data.removeRepositories.resources.repositories),
              },
              type: actionTypes.LOAD_RESOURCES,
            });
            msgSuccess(
              translate.t("search_findings.tab_resources.success_remove"),
              translate.t("search_findings.tab_users.title_success"),
            );
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred removing repositories");
          }
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;

            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error(error.message, errors);
          }
        });
    };

export const saveEnvs: ((projectName: string, envsData: IResources["environments"]) => ThunkResult<void>) =
  (projectName: string, envsData: IResources["environments"]): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
          addEnvironments (
            resourcesData: ${JSON.stringify(JSON.stringify(envsData))},
            projectName: "${projectName}") {
            success
            resources {
              environments
              files
              repositories
            }
          }
        }`;
      new Xhr().request(gQry, "An error occurred adding environments")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.addEnvironments.success) {
            dispatch(closeAddEnvModal());
            dispatch({
              payload: {
                environments: JSON.parse(data.addEnvironments.resources.environments),
                files: JSON.parse(data.addEnvironments.resources.files),
                repositories: JSON.parse(data.addEnvironments.resources.repositories),
              },
              type: actionTypes.LOAD_RESOURCES,
            });
            msgSuccess(
              translate.t("search_findings.tab_resources.success"),
              translate.t("search_findings.tab_users.title_success"),
            );
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred adding repositories");
          }
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;

            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error(error.message, errors);
          }
        });
    };

export const removeEnv: ((projectName: string, envToRemove: string) => ThunkResult<void>) =
  (projectName: string, envToRemove: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
      removeEnvironments (
        repositoryData: ${JSON.stringify(JSON.stringify({ urlEnv: envToRemove }))},
        projectName: "${projectName}"
      ) {
        success
        resources {
          environments
          files
          repositories
        }
      }
    }`;
      new Xhr().request(gQry, "An error occurred removing environments")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.removeEnvironments.success) {
            dispatch({
              payload: {
                environments: JSON.parse(data.removeEnvironments.resources.environments),
                files: JSON.parse(data.removeEnvironments.resources.files),
                repositories: JSON.parse(data.removeEnvironments.resources.repositories),
              },
              type: actionTypes.LOAD_RESOURCES,
            });
            msgSuccess(
              translate.t("search_findings.tab_resources.success_remove"),
              translate.t("search_findings.tab_users.title_success"),
            );
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred removing environments");
          }
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;

            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error(error.message, errors);
          }
        });
    };
export const uploadProgress: ((percentCompleted: number | undefined) => IActionStructure) =
  (percentCompleted: number | undefined): IActionStructure =>
  ({
    payload: { percentCompleted },
    type: actionTypes.UPDATE_UPLOAD_PROGRESS,
  });

export const showUploadProgress: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.SHOW_UPLOAD_PROGRESS,
  });

export const saveFiles: ((projectName: string, filesData: IResources["files"]) => ThunkResult<void>) =
  (projectName: string, filesData: IResources["files"]): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      dispatch(showUploadProgress());
      const uploadProgressDispatch: ((percentCompleted: number) => void) =
        (percentCompleted: number): void  => {
          dispatch(uploadProgress(percentCompleted));
      };

      gQry = `mutation {
          addFiles (
            filesData: ${JSON.stringify(JSON.stringify(filesData))},
            projectName: "${projectName}") {
            success
            resources {
              environments
              files
              repositories
            }
          }
        }`;
      new Xhr().upload(gQry, "#file", "An error occurred adding file", uploadProgressDispatch)
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.addFiles.success) {
            dispatch(closeAddFilesModal());
            dispatch(showUploadProgress());
            dispatch({
              payload: {
                environments: JSON.parse(data.addFiles.resources.environments),
                files: JSON.parse(data.addFiles.resources.files),
                repositories: JSON.parse(data.addFiles.resources.repositories),
              },
              type: actionTypes.LOAD_RESOURCES,
            });
            msgSuccess(
              translate.t("search_findings.tab_resources.success"),
              translate.t("search_findings.tab_users.title_success"),
            );
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred adding files");
          }
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;
            switch (errors[0].message) {
              case "File exceeds the size limits":
                msgError(translate.t("validations.file_size", { count: 100 }));
                break;
              case "Error uploading file":
                msgError(translate.t("search_findings.tab_resources.no_file_upload"));
                break;
              case "File already exist":
                msgError(translate.t("search_findings.tab_resources.repeated_item"));
                break;
              default:
                msgError(translate.t("proj_alerts.error_textsad"));
                rollbar.error(error.message, errors);
            }
          }
        });
    };

export const deleteFile: ((projectName: string, fileToRemove: string) => ThunkResult<void>) =
      (projectName: string, fileToRemove: string): ThunkResult<void> =>
        (dispatch: ThunkDispatcher): void => {
          let gQry: string;
          gQry = `mutation {
          removeFiles (
            filesData: ${JSON.stringify(JSON.stringify({ fileName: fileToRemove }))},
            projectName: "${projectName}"
          ) {
            success
            resources {
              environments
              files
              repositories
            }
          }
        }`;
          new Xhr().request(gQry, "An error occurred deleting files")
            .then((response: AxiosResponse) => {
              const { data } = response.data;
              if (data.removeFiles.success) {
                dispatch(closeOptionsModal());
                dispatch({
                  payload: {
                    environments: JSON.parse(data.removeFiles.resources.environments),
                    files: JSON.parse(data.removeFiles.resources.files),
                    repositories: JSON.parse(data.removeFiles.resources.repositories),
                  },
                  type: actionTypes.LOAD_RESOURCES,
                });
                msgSuccess(
                  translate.t("search_findings.tab_resources.success_remove"),
                  translate.t("search_findings.tab_users.title_success"),
                );
              } else {
                msgError(translate.t("proj_alerts.error_textsad"));
                rollbar.error("An error occurred deleting files");
              }
            })
            .catch((error: AxiosError) => {
              if (error.response !== undefined) {
                const { errors } = error.response.data;
                msgError(translate.t("proj_alerts.error_textsad"));
                rollbar.error(error.message, errors);
              }
            });
        };

export const downloadFile: ((projectName: string, fileToDownload: string) => ThunkResult<void>) =
      (projectName: string, fileToDownload: string): ThunkResult<void> =>
        (dispatch: ThunkDispatcher): void => {
          let gQry: string;
          gQry = `mutation {
              downloadFile (
                filesData: ${JSON.stringify(JSON.stringify(fileToDownload))},
                projectName: "${projectName}") {
                success
                url
              }
            }`;
          new Xhr().request(gQry, "An error occurred downloading file")
            .then((response: AxiosResponse) => {
              const { data } = response.data;
              if (data.downloadFile.success) {
                dispatch(closeOptionsModal());
                window.open(data.downloadFile.url);
              } else {
                msgError(translate.t("proj_alerts.error_textsad"));
                rollbar.error("An error occurred downloading files");
              }
            })
            .catch((error: AxiosError) => {
              if (error.response !== undefined) {
                const { errors } = error.response.data;
                msgError(translate.t("proj_alerts.error_textsad"));
                rollbar.error(error.message, errors);
              }
            });
        };

export const openTagsModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_TAGS_MODAL,
  });

export const closeTagsModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_TAGS_MODAL,
  });
