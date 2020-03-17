import { AxiosError, AxiosResponse } from "axios";
import _ from "lodash";
import { Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import * as actionTypes from "./actionTypes";
import { IDescriptionViewProps } from "./index";

export interface IActionStructure {
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the payload
   * type may differ between actions
   */
  payload: any;
  type: string;
}

type ThunkDispatcher = Dispatch<IActionStructure> & ThunkDispatch<{}, {}, IActionStructure>;
/* tslint:disable-next-line:no-any
 * Disabling this rule is necessary because the args
 * of an async action may differ
 */
type ThunkActionStructure<T> = ((...args: any[]) => ThunkAction<T, {}, {}, IActionStructure>);

export const editDescription: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.EDIT_DESCRIPTION,
  });

export const openRemediationMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.OPEN_REMEDIATION_MDL,
  });

export const closeRemediationMdl: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLOSE_REMEDIATION_MDL,
  });

export const clearDescription: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CLEAR_DESCRIPTION,
  });

export const loadDescription: ThunkActionStructure<void> =
  (findingId: string, projectName: string, userRole: string): ThunkAction<void, {}, {}, IActionStructure> =>
    (dispatch: ThunkDispatcher): void => {
      const canEditTreatmentMgr: boolean = _.includes(["customeradmin"], userRole);
      let gQry: string;
      const analystField: boolean = _.includes(["analyst", "admin"], userRole);
      gQry = `{
        project(projectName: "${projectName}") {
          subscription
          userEmails: users @include(if: ${canEditTreatmentMgr}) {
            email
          }
        }
        finding(identifier: "${findingId}") {
          analyst @include(if: ${analystField})
        }
      }`;

      new Xhr().request(gQry, "An error occurred getting finding description")
        .then((response: AxiosResponse) => {
          const { data } = response.data;

          dispatch<IActionStructure>({
            payload: {
              descriptionData: { ...data.finding, ...data.project },
            },
            type: actionTypes.LOAD_DESCRIPTION,
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

export const updateDescription: ThunkActionStructure<void> =
  (findingId: string, values: IDescriptionViewProps["dataset"]): ThunkAction<void, {}, {}, IActionStructure> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
        updateDescription(
          actor: ${JSON.stringify(values.actor)},
          affectedSystems: ${JSON.stringify(values.affectedSystems)},
          attackVectorDesc: ${JSON.stringify(values.attackVectorDesc)},
          cwe: ${JSON.stringify(values.cweUrl)},
          description: ${JSON.stringify(values.description)},
          findingId: "${findingId}",
          recommendation: ${JSON.stringify(values.recommendation)},
          records: ${JSON.stringify(values.compromisedAttributes)},
          recordsNumber: ${values.compromisedRecords},
          requirements: ${JSON.stringify(values.requirements)},
          scenario: ${JSON.stringify(values.scenario)},
          threat: ${JSON.stringify(values.threat)},
          title: ${JSON.stringify(values.title)},
          findingType: ${JSON.stringify(values.type)}
        ) {
          finding {
            actor
            affectedSystems
            attackVectorDesc
            cweUrl
            description
            recommendation
            compromisedAttributes
            compromisedRecords
            requirements
            scenario
            threat
            title
            risk
            type
          }
          success
        }
      }`;

      new Xhr().request(gQry, "An error occurred updating finding description")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.updateDescription.success) {
            dispatch<IActionStructure>({
              payload: {
                descriptionData: data.updateDescription.finding,
              },
              type: actionTypes.LOAD_DESCRIPTION,
            });
            dispatch<IActionStructure>(editDescription());
            msgSuccess(
              translate.t("proj_alerts.updated"),
              translate.t("proj_alerts.updated_title"),
            );
            // Temporary during the migration of this mutation to apollo
            location.reload();
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
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

export const updateClientDescription: ThunkActionStructure<void> =
  (findingId: string, values: IDescriptionViewProps["dataset"]): ThunkAction<void, {}, {}, IActionStructure> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      const treatment: string = values.treatment;
      let accAppr: string = values.acceptationApproval;
      accAppr = "";
      if (treatment === "ACCEPTED_UNDEFINED") {
        accAppr = "SUBMITTED";
      }
      gQry = `mutation {
        updateClientDescription(
          btsUrl: ${JSON.stringify(values.btsUrl)},
          findingId: "${findingId}",
          treatment: "${treatment}",
          justification: ${JSON.stringify(values.justification)},
          acceptanceDate: "${values.acceptanceDate}",
          acceptanceStatus: "${accAppr}"
        ) {
          finding {
            btsUrl
            historicTreatment
          }
          success
        }
      }`;

      new Xhr().request(gQry, "An error occurred updating finding description")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.updateClientDescription.success) {
            const nStates: number = data.updateClientDescription.finding.historicTreatment.length;
            if ("treatment" in data.updateClientDescription.finding
                                                           .historicTreatment[nStates - 1]) {
              data.updateClientDescription.finding.treatment =
                data.updateClientDescription.finding.historicTreatment[nStates - 1].treatment;
            }
            if ("acceptance_date" in data.updateClientDescription.finding
                                         .historicTreatment[nStates - 1]) {
              data.updateClientDescription.finding.acceptanceDate =
                data.updateClientDescription.finding.historicTreatment[nStates - 1]
                .acceptance_date.split(" ")[0];
            }
            if ("acceptance_status" in data.updateClientDescription
                                           .finding.historicTreatment[nStates - 1]) {
              data.updateClientDescription.finding.acceptationApproval =
                data.updateClientDescription.finding
                                            .historicTreatment[nStates - 1].acceptance_status;
            }
            if ("justification" in data.updateClientDescription.finding
                                                               .historicTreatment[nStates - 1]) {
              data.updateClientDescription.finding.justification =
                data.updateClientDescription.finding.historicTreatment[nStates - 1].justification;
            }
            dispatch<IActionStructure>({
              payload: {
                descriptionData: data.updateClientDescription.finding,
              },
              type: actionTypes.LOAD_DESCRIPTION,
            });
            msgSuccess(
              translate.t("proj_alerts.updated"),
              translate.t("proj_alerts.updated_title"),
            );
            dispatch<IActionStructure>(editDescription());
            // Temporary during the migration of this mutation to apollo
            location.reload();
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
          }
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;
            if (errors[0].message === "Invalid treatment manager") {
              msgError(translate.t("proj_alerts.invalid_treatment_mgr"));
            } else if (errors[0].message === "Exception - The inserted date is invalid") {
              msgError(translate.t("proj_alerts.invalid_date"));
            } else {
              msgError(translate.t("proj_alerts.error_textsad"));
              rollbar.error(error.message, errors);
            }
          }
        });
    };
