import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import * as actionTypes from "./actionTypes";
import { IIndicatorsViewProps } from "./index";

export interface IActionStructure {
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the payload
   * type may differ between actions
   */
  payload: any;
  type: string;
}

type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;
/* tslint:disable-next-line:no-any
 * Disabling this rule is necessary because the args
 * of an async action may differ
 */
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, AnyAction>);

export const clearTags: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLEAR_TAGS,
  });

export const loadIndicators: ThunkActionStructure =
  (projectName: IIndicatorsViewProps["projectName"]): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
      dispatch(clearTags());
      let gQry: string;
      gQry = `{
        project(projectName: "${projectName}"){
          closedPercentage
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
          undefinedTreatment
        }
      }`;
      new Xhr().request(gQry, "An error occurred getting tags")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          dispatch({
            payload: {
              closedPercentage: data.project.closedPercentage,
              closedVulnerabilities: data.project.closedVulnerabilities,
              deletionDate: data.project.deletionDate,
              lastClosingVuln: data.project.lastClosingVuln,
              maxOpenSeverity: data.project.maxOpenSeverity,
              maxSeverity: data.project.maxSeverity,
              meanRemediate: data.project.meanRemediate,
              openVulnerabilities: data.project.openVulnerabilities,
              pendingClosingCheck: data.project.pendingClosingCheck,
              subscription: data.project.subscription,
              tags: data.project.tags,
              totalFindings: data.project.totalFindings,
              undefinedTreatment: data.project.undefinedTreatment,
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

export const removeTag: ThunkActionStructure =
  (projectName: string, tagToRemove: string): ThunkAction<void, {}, {}, Action> =>
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
                tags: data.removeTag.project.tags,
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

export const saveTags: ThunkActionStructure =
  (projectName: string,
   tagsData: IIndicatorsViewProps["tagsDataset"]): ThunkAction<void, {}, {}, Action> =>
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
                tags: data.addTags.project.tags,
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
