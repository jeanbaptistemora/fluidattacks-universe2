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
        project(projectName: "${projectName}"){
          deletionDate
          subscription
        }
        resources (projectName: "${projectName}") {
          files
        }
      }`;
      new Xhr().request(gQry, "An error occurred getting repositories")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          dispatch({
            payload: {
              files: JSON.parse(data.resources.files),
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

export const changeSortedValues: ((newValues: {}) => IActionStructure) = (newValues: {}): IActionStructure => ({
    payload: {
      defaultSort: {
        ...newValues,
      },
    },
    type: actionTypes.CHANGE_SORTED,
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
            projectName: "${projectName}", file: "") {
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
                const newTab: Window | null = window.open(data.downloadFile.url);
                (newTab as typeof window).opener = undefined;
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
