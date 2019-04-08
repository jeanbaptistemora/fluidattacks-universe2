import { AxiosError, AxiosResponse } from "axios";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import { IDashboardState } from "../../reducer";
import * as actionTypes from "./actionTypes";

type IIndicators = IDashboardState["indicators"];

export interface IActionStructure {
  payload?: { [key: string]: string | string[] };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

type ThunkResult<T> = ThunkAction<T, {}, undefined, IActionStructure>;

export const loadIndicators: ((projectName: string) => ThunkResult<void>) =
  (projectName: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `{
        project(projectName: "${projectName}"){
          closedVulnerabilities
          deletionDate
          lastClosingVuln
          maxOpenSeverity
          maxSeverity
          meanRemediate
          openVulnerabilities
          pendingClosingCheck
          subscription
          tags
          totalFindings
          totalTreatment
        }
      }`;
      new Xhr().request(gQry, "An error occurred getting tags")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          dispatch({
            payload: {
              closedVulnerabilities: data.project.closedVulnerabilities,
              deletionDate: data.project.deletionDate,
              lastClosingVuln: data.project.lastClosingVuln,
              maxOpenSeverity: data.project.maxOpenSeverity,
              maxSeverity: data.project.maxSeverity,
              meanRemediate: data.project.meanRemediate,
              openVulnerabilities: data.project.openVulnerabilities,
              pendingClosingCheck: data.project.pendingClosingCheck,
              subscription: data.project.subscription,
              tagsDataset: data.project.tags,
              totalFindings: data.project.totalFindings,
              totalTreatment: data.project.totalTreatment,
            },
            type: actionTypes.LOAD_INDICATORS,
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

export const openAddModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_ADD_MODAL,
  });

export const closeAddModal: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_ADD_MODAL,
  });

export const removeTag: ((projectName: string, tagToRemove: string) => ThunkResult<void>) =
  (projectName: string, tagToRemove: string): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
        removeTag (
          tag: "${tagToRemove}",
          projectName: "${projectName}"
        ) {
          success
          project {
            deletionDate
            subscription
            tags
          }
        }
      }`;
      new Xhr().request(gQry, "An error occurred removing tags")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.removeTag.success) {
            dispatch({
              payload: {
                deletionDate: data.removeTag.project.deletionDate,
                subscription: data.removeTag.project.subscription,
                tagsDataset: data.removeTag.project.tags,
              },
              type: actionTypes.LOAD_INDICATORS,
            });
            msgSuccess(
              translate.t("search_findings.tab_resources.success_remove"),
              translate.t("search_findings.tab_users.title_success"),
            );
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred removing tags");
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

export const saveTags: ((projectName: string, tagsData: IIndicators["tagsDataset"]) => ThunkResult<void>) =
  (projectName: string, tagsData: IIndicators["tagsDataset"]): ThunkResult<void> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
          addTags (
            tags: ${JSON.stringify(JSON.stringify(tagsData))},
            projectName: "${projectName}") {
            success
            project {
              deletionDate
              subscription
              tags
            }
          }
        }`;
      new Xhr().request(gQry, "An error occurred adding tags")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.addTags.success) {
            dispatch(closeAddModal());
            dispatch({
              payload: {
                deletionDate: data.addTags.project.deletionDate,
                subscription: data.addTags.project.subscription,
                tagsDataset: data.addTags.project.tags,
              },
              type: actionTypes.LOAD_INDICATORS,
            });
            msgSuccess(
              translate.t("search_findings.tab_resources.success"),
              translate.t("search_findings.tab_users.title_success"),
            );
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred adding tags");
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
