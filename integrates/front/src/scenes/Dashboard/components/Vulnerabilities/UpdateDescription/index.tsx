import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useContext, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import type { Dispatch } from "redux";
import { formValueSelector, isPristine, submit } from "redux-form";

import { AcceptanceDateField } from "./AcceptanceDateField";
import { AcceptationUserField } from "./AcceptationUserField";
import { ExternalBtsField } from "./ExternalBtsField";
import {
  dataTreatmentTrackHelper,
  deleteTagVulnHelper,
  getAreAllMutationValid,
  getResults,
  handleRequestZeroRiskError,
  handleSubmitHelper,
  handleUpdateTreatmentVulnError,
  hasNewVulnsAlert,
  isTheFormPristine,
  requestZeroRiskHelper,
  treatmentChangeAlert,
  validMutationsHelper,
} from "./helpers";
import { JustificationField } from "./JustificationField";
import { SeverityField } from "./SeverityField";
import { TagField } from "./TagField";
import { TreatmentField } from "./TreatmentField";
import { TreatmentManagerField } from "./TreatmentManagerField";

import { GET_FINDING_HEADER } from "../../../containers/FindingContent/queries";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { IConfirmFn } from "components/ConfirmDialog";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { GET_PROJECT_USERS } from "scenes/Dashboard/components/Vulnerabilities/queries";
import type {
  IUpdateTreatmentVulnAttr,
  IVulnDataTypeAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  DELETE_TAGS_MUTATION,
  REQUEST_ZERO_RISK_VULN,
  UPDATE_DESCRIPTION_MUTATION,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/queries";
import type {
  IDeleteTagAttr,
  IDeleteTagResultAttr,
  IProjectUsersAttr,
  IRequestZeroRiskVulnResultAttr,
  IStakeholderAttr,
  IUpdateTreatmentModalProps,
  IUpdateVulnDescriptionResultAttr,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";
import {
  groupExternalBts,
  groupLastHistoricTreatment,
  groupVulnLevel,
  hasNewTreatment,
  sortTags,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { ButtonToolbar, Col100, Col50, Row } from "styles/styledComponents";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const UpdateTreatmentModal: React.FC<IUpdateTreatmentModalProps> = ({
  findingId,
  projectName,
  vulnerabilities,
  handleClearSelected,
  handleCloseModal,
}: IUpdateTreatmentModalProps): JSX.Element => {
  const { userEmail }: IAuthContext = useContext(authContext);
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveAnalyst: boolean = permissions.can(
    "api_resolvers_vulnerability_analyst_resolve"
  );
  const canRetrieveZeroRisk: boolean = permissions.can(
    "api_resolvers_finding_zero_risk_resolve"
  );
  const canGetHistoricState: boolean = permissions.can(
    "api_resolvers_finding_historic_state_resolve"
  );
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "api_mutations_request_zero_risk_vuln_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulns_treatment_mutate"
  );
  const [isRunning, setRunning] = useState(false);

  const vulnsTags: string[][] = vulnerabilities.map(
    (vuln: IVulnDataTypeAttr): string[] => sortTags(vuln.tag)
  );
  const isEditPristine: boolean = useSelector(
    (state: Record<string, unknown>): boolean =>
      isPristine("editTreatmentVulnerability")(
        state,
        ...["externalBts", "tag", "severity"]
      )
  );

  const isTreatmentValuesPristine: boolean = useSelector(
    (state: Record<string, unknown>): boolean =>
      isPristine("editTreatmentVulnerability")(
        state,
        ...["acceptanceDate", "treatment", "treatmentManager"]
      )
  );
  const formValues: Dictionary<string> = useSelector(
    (state: Record<string, unknown>): Dictionary<string> =>
      // It is necessary since formValueSelector returns an any type
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return
      formValueSelector("editTreatmentVulnerability")(
        state,
        "treatment",
        "justification",
        ""
      )
  );

  const isTreatmentPristine = isTheFormPristine(
    isTreatmentValuesPristine,
    formValues,
    vulnerabilities
  );

  const dispatch: Dispatch = useDispatch();
  const [updateVuln, { loading: updatingVuln }] =
    useMutation<IUpdateVulnDescriptionResultAttr>(UPDATE_DESCRIPTION_MUTATION, {
      refetchQueries: [
        {
          query: GET_FINDING_VULN_INFO,
          variables: {
            canRetrieveAnalyst,
            canRetrieveZeroRisk,
            findingId,
            groupName: projectName,
          },
        },
      ],
    });

  const { data } = useQuery<IProjectUsersAttr>(GET_PROJECT_USERS, {
    skip: permissions.cannot("api_resolvers_project__get_users"),
    variables: {
      projectName,
    },
  });

  const [deleteTagVuln, { loading: deletingTag }] = useMutation<
    IDeleteTagResultAttr,
    IDeleteTagAttr
  >(DELETE_TAGS_MUTATION, {
    onCompleted: (result: IDeleteTagResultAttr): void => {
      deleteTagVulnHelper(result);
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred deleting vulnerabilities", error);
      });
    },
    refetchQueries: [
      {
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveAnalyst,
          canRetrieveZeroRisk,
          findingId,
          groupName: projectName,
        },
      },
    ],
  });

  const handleUpdateTreatmentVuln = async (
    dataTreatment: IUpdateTreatmentVulnAttr
  ): Promise<void> => {
    if (vulnerabilities.length === 0) {
      msgError(translate.t("searchFindings.tabResources.noSelection"));
    } else {
      dataTreatmentTrackHelper(dataTreatment);
      try {
        setRunning(true);
        const results = await getResults(
          updateVuln,
          vulnerabilities,
          dataTreatment,
          findingId,
          isEditPristine,
          isTreatmentPristine
        );

        const areAllMutationValid = getAreAllMutationValid(results);

        validMutationsHelper(
          handleCloseModal,
          areAllMutationValid,
          vulnerabilities
        );
      } catch (updateError: unknown) {
        handleUpdateTreatmentVulnError(updateError);
      } finally {
        setRunning(false);
      }
    }
  };

  function handleEditTreatment(): void {
    dispatch(submit("editTreatmentVulnerability"));
  }

  function handleDeletion(tag: string): void {
    // Exception: FP(void operator is necessary)
    // eslint-disable-next-line
    void deleteTagVuln({ //NOSONAR
      variables: {
        findingId,
        tag,
        vulnerabilities: vulnerabilities.map(
          (vuln: IVulnDataTypeAttr): string => vuln.id
        ),
      },
    });
  }

  const [requestZeroRisk, { loading: requestingZeroRisk }] = useMutation(
    REQUEST_ZERO_RISK_VULN,
    {
      onCompleted: (
        requestZeroRiskVulnResult: IRequestZeroRiskVulnResultAttr
      ): void => {
        requestZeroRiskHelper(
          handleClearSelected,
          handleCloseModal,
          requestZeroRiskVulnResult
        );
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        handleRequestZeroRiskError(graphQLErrors);
      },
      refetchQueries: [
        {
          query: GET_FINDING_VULN_INFO,
          variables: {
            canRetrieveAnalyst,
            canRetrieveZeroRisk,
            findingId,
            groupName: projectName,
          },
        },
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetHistoricState,
            findingId,
          },
        },
      ],
    }
  );

  const userEmails: string[] =
    _.isUndefined(data) || _.isEmpty(data)
      ? [userEmail]
      : data.project.stakeholders.map(
          (stakeholder: IStakeholderAttr): string => stakeholder.email
        );

  const lastTreatment: IHistoricTreatment = {
    ...groupLastHistoricTreatment(vulnerabilities),
    justification: "",
  };

  const hasNewVulns: boolean = hasNewTreatment(vulnerabilities);

  const isInProgressSelected: boolean = formValues.treatment === "IN_PROGRESS";
  const isAcceptedSelected: boolean = formValues.treatment === "ACCEPTED";
  const isAcceptedUndefinedSelected: boolean =
    formValues.treatment === "ACCEPTED_UNDEFINED";

  return (
    <React.StrictMode>
      <React.StrictMode>
        <ConfirmDialog
          message={translate.t("searchFindings.tabDescription.approvalMessage")}
          title={translate.t("searchFindings.tabDescription.approvalTitle")}
        >
          {(confirm: IConfirmFn): JSX.Element => {
            function handleSubmit(values: IUpdateTreatmentVulnAttr): void {
              const changedToRequestZeroRisk: boolean =
                values.treatment === "REQUEST_ZERO_RISK";
              const changedToUndefined: boolean =
                values.treatment === "ACCEPTED_UNDEFINED" &&
                lastTreatment.treatment !== "ACCEPTED_UNDEFINED";

              handleSubmitHelper(
                handleUpdateTreatmentVuln,
                requestZeroRisk,
                confirm,
                values,
                findingId,
                vulnerabilities,
                changedToRequestZeroRisk,
                changedToUndefined
              );
            }

            return (
              <React.Fragment>
                <GenericForm
                  initialValues={{
                    ...lastTreatment,
                    externalBts: groupExternalBts(vulnerabilities),
                    severity: groupVulnLevel(vulnerabilities),
                    tag: _.join(_.intersection(...vulnsTags), ","),
                    treatment: lastTreatment.treatment.replace("NEW", ""),
                  }}
                  name={"editTreatmentVulnerability"}
                  onSubmit={handleSubmit}
                >
                  <Row>
                    <Col50>
                      <TreatmentField
                        isTreatmentPristine={isTreatmentPristine}
                        lastTreatment={lastTreatment}
                      />
                    </Col50>
                    <Col50>
                      <AcceptationUserField
                        isAcceptedSelected={isAcceptedSelected}
                        isAcceptedUndefinedSelected={
                          isAcceptedUndefinedSelected
                        }
                        isInProgressSelected={isInProgressSelected}
                        lastTreatment={lastTreatment}
                      />
                    </Col50>
                  </Row>
                  <Row>
                    <Col50>
                      <TreatmentManagerField
                        isInProgressSelected={isInProgressSelected}
                        lastTreatment={lastTreatment}
                        userEmails={userEmails}
                      />
                    </Col50>
                  </Row>
                  <Row>
                    <Col100>
                      <JustificationField
                        isTreatmentPristine={isTreatmentPristine}
                        lastTreatment={lastTreatment}
                      />
                    </Col100>
                  </Row>
                  <Row>
                    <Col50>
                      <AcceptanceDateField
                        isAcceptedSelected={isAcceptedSelected}
                        lastTreatment={lastTreatment}
                      />
                    </Col50>
                  </Row>
                  <Row>
                    <Col100>
                      <ExternalBtsField
                        hasNewVulnSelected={hasNewVulns}
                        isAcceptedSelected={isAcceptedSelected}
                        isAcceptedUndefinedSelected={
                          isAcceptedUndefinedSelected
                        }
                        isInProgressSelected={isInProgressSelected}
                        vulnerabilities={vulnerabilities}
                      />
                    </Col100>
                  </Row>
                  <Row>
                    <Col100>
                      <TagField
                        handleDeletion={handleDeletion}
                        hasNewVulnSelected={hasNewVulns}
                        isAcceptedSelected={isAcceptedSelected}
                        isAcceptedUndefinedSelected={
                          isAcceptedUndefinedSelected
                        }
                        isInProgressSelected={isInProgressSelected}
                      />
                    </Col100>
                  </Row>
                  <Row>
                    <Col50>
                      <SeverityField
                        hasNewVulnSelected={hasNewVulns}
                        isAcceptedSelected={isAcceptedSelected}
                        isAcceptedUndefinedSelected={
                          isAcceptedUndefinedSelected
                        }
                        isInProgressSelected={isInProgressSelected}
                        level={groupVulnLevel(vulnerabilities)}
                      />
                    </Col50>
                  </Row>
                </GenericForm>
                {treatmentChangeAlert(isTreatmentPristine)}
                {hasNewVulnsAlert(
                  vulnerabilities,
                  hasNewVulns,
                  isAcceptedSelected,
                  isAcceptedUndefinedSelected,
                  isInProgressSelected
                )}
                <hr />
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button onClick={handleCloseModal}>
                        {translate.t("group.findings.report.modalClose")}
                      </Button>
                      {canRequestZeroRiskVuln || canUpdateVulnsTreatment ? (
                        <Button
                          disabled={
                            requestingZeroRisk ||
                            updatingVuln ||
                            deletingTag ||
                            isRunning ||
                            (isEditPristine && isTreatmentPristine)
                          }
                          onClick={handleEditTreatment}
                        >
                          {translate.t("confirmmodal.proceed")}
                        </Button>
                      ) : undefined}
                    </ButtonToolbar>
                  </Col100>
                </Row>
              </React.Fragment>
            );
          }}
        </ConfirmDialog>
      </React.StrictMode>
    </React.StrictMode>
  );
};

export { UpdateTreatmentModal };
