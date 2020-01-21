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
    type: actionTypes.CLEAR_EVIDENCE,
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
          title
          scenario
          actor
          analyst @include(if: ${analystField})
          description
          requirements
          attackVectorDesc
          threat
          recommendation
          releaseDate
          remediated
          state
          affectedSystems
          compromisedAttributes
          compromisedRecords
          cweUrl
          btsUrl
          risk
          type
          openVulnerabilities
          historicTreatment
        }
      }`;

      new Xhr().request(gQry, "An error occurred getting finding description")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          const nStates: number = data.finding.historicTreatment.length;
          data.finding.acceptanceDate = "-";
          if ("acceptance_date" in data.finding.historicTreatment[nStates - 1]) {
            data.finding.acceptanceDate = data.finding.historicTreatment[nStates - 1].acceptance_date;
          }
          if ("acceptance_status" in data.finding.historicTreatment[nStates - 1]) {
            data.finding.acceptationApproval = data.finding.historicTreatment[nStates - 1].acceptance_status;
          }
          if ("treatment" in data.finding.historicTreatment[nStates - 1]) {
            data.finding.treatment = data.finding.historicTreatment[nStates - 1].treatment;
          }
          if ("justification" in data.finding.historicTreatment[nStates - 1]) {
            data.finding.justification = data.finding.historicTreatment[nStates - 1].justification;
          }
          if ("user" in data.finding.historicTreatment[nStates - 1]) {
            data.finding.acceptationUser = data.finding.historicTreatment[nStates - 1].user;
          }
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

export const requestVerification: ThunkActionStructure<void> =
  (findingId: string, justification: string): ThunkAction<void, {}, {}, IActionStructure> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
        requestVerification(
          findingId: "${findingId}",
          justification: ${JSON.stringify(justification)}
        ) {
          success
        }
      }`;

      new Xhr().request(gQry, "An error occurred requesting verification")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.requestVerification.success) {
            dispatch<IActionStructure>({
              payload: {
                descriptionData: { remediated: true },
              },
              type: actionTypes.LOAD_DESCRIPTION,
            });
            dispatch<IActionStructure>(closeRemediationMdl());
            msgSuccess(
              translate.t("proj_alerts.verified_success"),
              translate.t("proj_alerts.updated_title"),
            );
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred verifying finding");
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

export const verifyFinding: ThunkActionStructure<void> =
  (findingId: string): ThunkAction<void, {}, {}, IActionStructure> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
        verifyFinding(findingId: "${findingId}") {
          success
        }
      }`;

      new Xhr().request(gQry, "An error occurred verifying finding")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.verifyFinding.success) {
            dispatch<IActionStructure>({
              payload: {
                descriptionData: { remediated: false },
              },
              type: actionTypes.LOAD_DESCRIPTION,
            });
            msgSuccess(
              translate.t("proj_alerts.verified_success"),
              translate.t("proj_alerts.updated_title"),
            );
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred verifying finding");
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

export const updateTreatment: ThunkActionStructure<void> =
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
        updateTreatment(
          btsUrl: ${JSON.stringify(values.btsUrl)},
          findingId: "${findingId}",
          treatment: "${treatment}",
          justification: ${JSON.stringify(values.justification)},
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
          if (data.updateTreatment.success) {
            const nStates: number = data.updateTreatment.finding.historicTreatment.length;
            if ("treatment" in data.updateTreatment.finding.historicTreatment[nStates - 1]) {
              data.updateTreatment.finding.treatment =
                data.updateTreatment.finding.historicTreatment[nStates - 1].treatment;
            }
            if ("acceptance_date" in data.updateTreatment.finding.historicTreatment[nStates - 1]) {
              data.updateTreatment.finding.acceptanceDate =
                data.updateTreatment.finding.historicTreatment[nStates - 1].acceptance_date;
            }
            if ("acceptance_status" in data.updateTreatment.finding.historicTreatment[nStates - 1]) {
              data.updateTreatment.finding.acceptationApproval =
                data.updateTreatment.finding.historicTreatment[nStates - 1].acceptance_status;
            }
            if ("justification" in data.updateTreatment.finding.historicTreatment[nStates - 1]) {
              data.updateTreatment.finding.justification =
                data.updateTreatment.finding.historicTreatment[nStates - 1].justification;
            }
            dispatch<IActionStructure>({
              payload: {
                descriptionData: data.updateTreatment.finding,
              },
              type: actionTypes.LOAD_DESCRIPTION,
            });
            msgSuccess(
              translate.t("proj_alerts.updated"),
              translate.t("proj_alerts.updated_title"),
            );
            dispatch<IActionStructure>(editDescription());
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
          }
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;
            if (errors[0].message === "Invalid treatment manager") {
              msgError(translate.t("proj_alerts.invalid_treatment_mgr"));
            } else {
              msgError(translate.t("proj_alerts.error_textsad"));
              rollbar.error(error.message, errors);
            }
          }
        });
    };
