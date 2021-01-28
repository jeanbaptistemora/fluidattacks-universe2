import { AcceptanceDateField } from "./AcceptanceDateField";
import { AcceptationUserField } from "./AcceptationUserField";
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { Dispatch } from "redux";
import { ExternalBtsField } from "./ExternalBtsField";
import { GET_FINDING_HEADER } from "../../../containers/FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { GET_PROJECT_USERS } from "scenes/Dashboard/components/Vulnerabilities/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { IAuthContext } from "utils/auth";
import type { IConfirmFn } from "components/ConfirmDialog";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { JustificationField } from "./JustificationField";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { SeverityField } from "./SeverityField";
import { TagField } from "./TagField";
import { TreatmentField } from "./TreatmentField";
import { TreatmentManagerField } from "./TreatmentManagerField";
import _ from "lodash";
import { authContext } from "utils/auth";
import mixpanel from "mixpanel-browser";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { ButtonToolbar, Col100, Col50, Row } from "styles/styledComponents";
import {
  DELETE_TAGS_MUTATION,
  REQUEST_ZERO_RISK_VULN,
  UPDATE_DESCRIPTION_MUTATION,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/queries";
import type { ExecutionResult, GraphQLError } from "graphql";
import type {
  IDeleteTagAttr,
  IDeleteTagResultAttr,
  IProjectUsersAttr,
  IRequestZeroRiskVulnResultAttr,
  IStakeholderAttr,
  IUpdateTreatmentModalProps,
  IUpdateVulnDescriptionResultAttr,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";
import type {
  IUpdateTreatmentVulnAttr,
  IVulnDataTypeAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { formValueSelector, isPristine, submit } from "redux-form";
import {
  groupExternalBts,
  groupLastHistoricTreatment,
  groupVulnLevel,
  sortTags,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import { msgError, msgSuccess } from "utils/notifications";
import { useDispatch, useSelector } from "react-redux";
import { useMutation, useQuery } from "@apollo/react-hooks";

const UpdateTreatmentModal: React.FC<IUpdateTreatmentModalProps> = ({
  findingId,
  projectName,
  vulnerabilities,
  handleClearSelected,
  handleCloseModal,
}: IUpdateTreatmentModalProps): JSX.Element => {
  const { userEmail, userName }: IAuthContext = React.useContext(authContext);
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveAnalyst: boolean = permissions.can(
    "backend_api_resolvers_vulnerability_analyst_resolve"
  );
  const canGetHistoricState: boolean = permissions.can(
    "backend_api_resolvers_finding_historic_state_resolve"
  );
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_request_zero_risk_vuln_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "backend_api_mutations_update_vulns_treatment_mutate"
  );
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);
  const canGetExploit: boolean = groupPermissions.can("has_forces");
  const [isRunning, setRunning] = React.useState(false);

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

  const isTreatmentPristine: boolean = useSelector(
    (state: Record<string, unknown>): boolean =>
      isPristine("editTreatmentVulnerability")(
        state,
        ...["acceptanceDate", "treatment", "treatmentManager", "justification"]
      )
  );

  const dispatch: Dispatch = useDispatch();
  const [updateVuln, { loading: updatingVuln }] = useMutation<
    IUpdateVulnDescriptionResultAttr
  >(UPDATE_DESCRIPTION_MUTATION, {
    refetchQueries: [
      {
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveAnalyst,
          findingId,
          groupName: projectName,
        },
      },
    ],
  });

  const { data } = useQuery<IProjectUsersAttr>(GET_PROJECT_USERS, {
    skip: permissions.cannot("backend_api_resolvers_project__get_users"),
    variables: {
      projectName: projectName,
    },
  });

  const [deleteTagVuln, { loading: deletingTag }] = useMutation<
    IDeleteTagResultAttr,
    IDeleteTagAttr
  >(DELETE_TAGS_MUTATION, {
    onCompleted: (result: IDeleteTagResultAttr): void => {
      if (!_.isUndefined(result)) {
        if (result.deleteTags.success) {
          msgSuccess(
            translate.t(
              "search_findings.tab_description.update_vulnerabilities"
            ),
            translate.t("group_alerts.title_success")
          );
        }
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred deleting vulnerabilities", error);
      });
    },
    refetchQueries: [
      {
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveAnalyst,
          findingId,
          groupName: projectName,
        },
      },
    ],
  });

  const handleUpdateTreatmentVuln: (
    dataTreatment: IUpdateTreatmentVulnAttr
  ) => Promise<void> = async (
    dataTreatment: IUpdateTreatmentVulnAttr
  ): Promise<void> => {
    if (vulnerabilities.length === 0) {
      msgError(translate.t("search_findings.tab_resources.no_selection"));
    } else {
      try {
        setRunning(true);
        const results: ExecutionResult<
          IUpdateVulnDescriptionResultAttr
        >[] = await Promise.all(
          vulnerabilities.map(
            async (
              vuln: IVulnDataTypeAttr
            ): Promise<ExecutionResult<IUpdateVulnDescriptionResultAttr>> =>
              updateVuln({
                variables: {
                  acceptanceDate: dataTreatment.acceptanceDate,
                  externalBts: dataTreatment.externalBts,
                  findingId: findingId,
                  isVulnInfoChanged: !isEditPristine,
                  isVulnTreatmentChanged: !isTreatmentPristine,
                  justification: dataTreatment.justification,
                  severity: _.isEmpty(dataTreatment.severity)
                    ? -1
                    : Number(dataTreatment.severity),
                  tag: dataTreatment.tag,
                  treatment: isTreatmentPristine
                    ? "IN_PROGRESS"
                    : dataTreatment.treatment,
                  treatmentManager:
                    _.isEmpty(dataTreatment.treatmentManager) ||
                    dataTreatment.treatment !== "IN_PROGRESS"
                      ? undefined
                      : dataTreatment.treatmentManager,
                  vulnerabilityId: vuln.id,
                },
              })
          )
        );

        const areAllMutationValid: boolean[] = results.map(
          (
            result: ExecutionResult<IUpdateVulnDescriptionResultAttr>
          ): boolean => {
            if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
              const updateInfoSuccess: boolean = _.isUndefined(
                result.data.updateTreatmentVuln
              )
                ? true
                : result.data.updateTreatmentVuln.success;
              const updateTreatmentSuccess: boolean = _.isUndefined(
                result.data.updateVulnsTreatment
              )
                ? true
                : result.data.updateVulnsTreatment.success;

              return updateInfoSuccess && updateTreatmentSuccess;
            }

            return false;
          }
        );

        if (areAllMutationValid.every(Boolean)) {
          mixpanel.track("UpdatedTreatmentVulnerabilities", { User: userName });
          msgSuccess(
            translate.t(
              "search_findings.tab_description.update_vulnerabilities"
            ),
            translate.t("group_alerts.title_success")
          );
          handleCloseModal();
        }
      } catch (updateError: unknown) {
        if (_.includes(String(updateError), "Invalid treatment manager")) {
          msgError(translate.t("group_alerts.invalid_treatment_mgr"));
        } else if (
          _.includes(
            String(updateError),
            translate.t(
              "search_findings.tab_vuln.alerts.maximum_number_of_acceptations"
            )
          )
        ) {
          msgError(
            translate.t(
              "search_findings.tab_vuln.alerts.maximum_number_of_acceptations"
            )
          );
        } else if (
          _.includes(
            String(updateError),
            translate.t(
              "group_alerts.organization_policies.exceeds_acceptance_date"
            )
          )
        ) {
          msgError(
            translate.t(
              "group_alerts.organization_policies.exceeds_acceptance_date"
            )
          );
        } else if (
          _.includes(
            String(updateError),
            translate.t(
              "search_findings.tab_vuln.exceptions.severity_out_of_range"
            )
          )
        ) {
          msgError(
            translate.t(
              "group_alerts.organization_policies.severity_out_of_range"
            )
          );
        } else {
          msgError(translate.t("group_alerts.error_textsad"));
          Logger.warning(
            "An error occurred updating vuln treatment",
            updateError
          );
        }
      } finally {
        setRunning(false);
      }
    }
  };

  function handleEditTreatment(): void {
    dispatch(submit("editTreatmentVulnerability"));
  }

  function handleDeletion(tag: string): void {
    void deleteTagVuln({
      variables: {
        findingId: findingId,
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
        if (requestZeroRiskVulnResult.requestZeroRiskVuln.success) {
          msgSuccess(
            translate.t("group_alerts.requested_zero_risk_success"),
            translate.t("group_alerts.updated_title")
          );
          handleClearSelected();
          handleCloseModal();
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - Zero risk vulnerability is already requested":
              msgError(translate.t("group_alerts.zero_risk_already_requested"));
              break;
            default:
              msgError(translate.t("group_alerts.error_textsad"));
              Logger.warning(
                "An error occurred requesting zero risk vuln",
                error
              );
          }
        });
      },
      refetchQueries: [
        {
          query: GET_FINDING_VULN_INFO,
          variables: {
            canRetrieveAnalyst,
            findingId,
            groupName: projectName,
          },
        },
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetExploit,
            canGetHistoricState,
            findingId: findingId,
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

  const formValues: Dictionary<string> = useSelector(
    (state: Record<string, unknown>): Dictionary<string> =>
      // It is necessary since formValueSelector returns an any type
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return
      formValueSelector("editTreatmentVulnerability")(state, "treatment", "")
  );

  const isInProgressSelected: boolean = formValues.treatment === "IN_PROGRESS";
  const isAcceptedSelected: boolean = formValues.treatment === "ACCEPTED";
  const isAcceptedUndefinedSelected: boolean =
    formValues.treatment === "ACCEPTED_UNDEFINED";

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("search_findings.tab_description.editVuln")}
        open={true}
      >
        <ConfirmDialog
          message={translate.t(
            "search_findings.tab_description.approval_message"
          )}
          title={translate.t("search_findings.tab_description.approval_title")}
        >
          {(confirm: IConfirmFn): JSX.Element => {
            function handleSubmit(values: IUpdateTreatmentVulnAttr): void {
              const changedToRequestZeroRisk: boolean =
                values.treatment === "REQUEST_ZERO_RISK";
              const changedToUndefined: boolean =
                values.treatment === "ACCEPTED_UNDEFINED" &&
                lastTreatment.treatment !== "ACCEPTED_UNDEFINED";

              if (changedToRequestZeroRisk) {
                void requestZeroRisk({
                  variables: {
                    findingId: findingId,
                    justification: values.justification,
                    vulnerabilities: vulnerabilities.map(
                      (vuln: IVulnDataTypeAttr): string => vuln.id
                    ),
                  },
                });
              } else if (changedToUndefined) {
                confirm((): void => {
                  void handleUpdateTreatmentVuln(values);
                });
              } else {
                void handleUpdateTreatmentVuln(values);
              }
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
                        isAcceptedSelected={isAcceptedSelected}
                        isAcceptedUndefinedSelected={
                          isAcceptedUndefinedSelected
                        }
                        isInProgressSelected={isInProgressSelected}
                      />
                    </Col50>
                  </Row>
                </GenericForm>
                <hr />
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button onClick={handleCloseModal}>
                        {translate.t("group.findings.report.modal_close")}
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
      </Modal>
    </React.StrictMode>
  );
};

export { UpdateTreatmentModal };
