/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch } from "redux";
import { Field, formValueSelector, isPristine, submit } from "redux-form";
import { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { ConfirmDialog, IConfirmFn } from "components/ConfirmDialog";
import { Modal } from "components/Modal";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  GET_PROJECT_USERS,
  GET_VULNERABILITIES,
} from "scenes/Dashboard/components/Vulnerabilities/queries";
import {
  IUpdateTreatmentVulnAttr,
  IVulnDataType,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  DELETE_TAGS_MUTATION,
  REQUEST_ZERO_RISK_VULN,
  UPDATE_DESCRIPTION_MUTATION,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/queries";
import {
  IDeleteTagAttr,
  IDeleteTagResultAttr,
  IRequestZeroRiskVulnResultAttr,
  IUpdateTreatmentModalProps,
  IUpdateVulnDescriptionResultAttr,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";
import {
  groupExternalBts,
  groupLastHistoricTreatment,
  groupVulnLevel,
  sortTags,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import {
  ButtonToolbar,
  Col100,
  Col50,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { formatDropdownField } from "utils/formatHelpers";
import { Date, Dropdown, TagInput, Text, TextArea } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  isLowerDate,
  isValidVulnSeverity,
  maxLength,
  numeric,
  required,
  validTextField,
  validUrlField,
} from "utils/validations";
import { GET_FINDING_HEADER } from "../../../containers/FindingContent/queries";

const maxBtsLength: ConfigurableValidator = maxLength(80);
const maxTreatmentJustificationLength: ConfigurableValidator = maxLength(200);
const updateTreatmentModal: React.FC<IUpdateTreatmentModalProps> = (
  props: IUpdateTreatmentModalProps,
): JSX.Element => {
  const { userEmail } = window as typeof window & Dictionary<string>;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDisplayAnalyst: boolean = permissions.can(
    "backend_api_resolvers_new_finding_analyst_resolve",
  );
  const canGetHistoricState: boolean = permissions.can(
    "backend_api_resolvers_new_finding_historic_state_resolve",
  );
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_request_zero_risk_vuln_mutate",
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "backend_api_mutations_update_vulns_treatment_mutate",
  );
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);
  const canGetExploit: boolean = groupPermissions.can("has_forces");
  const { handleClearSelected, handleCloseModal } = props;
  const [isRunning, setRunning] = React.useState(false);

  const vulnsTags: string[][] = props.vulnerabilities.map(
    (vuln: IVulnDataType) => sortTags(vuln.tag),
  );
  const isEditPristine: boolean = useSelector((state: {}) =>
    isPristine("editTreatmentVulnerability")(
      state,
      ...["externalBts", "tag", "severity"],
    ),
  );

  const isTreatmentPristine: boolean = useSelector((state: {}) =>
    isPristine("editTreatmentVulnerability")(
      state,
      ...["acceptanceDate", "treatment", "treatmentManager", "justification"],
    ),
  );

  const dispatch: Dispatch = useDispatch();
  const [updateVuln, { loading: updatingVuln }] = useMutation<
    IUpdateVulnDescriptionResultAttr
  >(UPDATE_DESCRIPTION_MUTATION, {
    refetchQueries: [
      {
        query: GET_VULNERABILITIES,
        variables: {
          analystField: permissions.can(
            "backend_api_resolvers_new_finding_analyst_resolve",
          ),
          identifier: props.findingId,
        },
      },
    ],
  });

  const { data } = useQuery(GET_PROJECT_USERS, {
    skip: permissions.cannot("backend_api_resolvers_project__get_users"),
    variables: {
      projectName: props.projectName,
    },
  });

  const [deleteTagVuln, { loading: deletingTag }] = useMutation<
    IDeleteTagResultAttr,
    IDeleteTagAttr
  >(DELETE_TAGS_MUTATION, {
    onCompleted: async (result: IDeleteTagResultAttr): Promise<void> => {
      if (!_.isUndefined(result)) {
        if (result.deleteTags.success) {
          msgSuccess(
            translate.t(
              "search_findings.tab_description.update_vulnerabilities",
            ),
            translate.t("group_alerts.title_success"),
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
        query: GET_VULNERABILITIES,
        variables: {
          analystField: permissions.can(
            "backend_api_resolvers_new_finding_analyst_resolve",
          ),
          identifier: props.findingId,
        },
      },
    ],
  });

  const handleUpdateTreatmentVuln: (
    dataTreatment: IUpdateTreatmentVulnAttr,
  ) => Promise<void> = async (
    dataTreatment: IUpdateTreatmentVulnAttr,
  ): Promise<void> => {
    if (props.vulnerabilities.length === 0) {
      msgError(translate.t("search_findings.tab_resources.no_selection"));
    } else {
      try {
        setRunning(true);
        const results: Array<ExecutionResult<
          IUpdateVulnDescriptionResultAttr
        >> = await Promise.all(
          // This comment is going to be removed
          // tslint:disable-next-line:newline-per-chained-call
          _.chunk(props.vulnerabilities, props.vulnerabilitiesChunk).map(
            (vulnsChuncked: IVulnDataType[]) =>
              updateVuln({
                variables: {
                  acceptanceDate: dataTreatment.acceptanceDate,
                  externalBts: dataTreatment.externalBts,
                  findingId: props.findingId,
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
                  vulnerabilities: vulnsChuncked.map(
                    (vuln: IVulnDataType) => vuln.id,
                  ),
                },
              }),
          ),
        );

        const areAllMutationValid: boolean[] = results.map(
          (result: ExecutionResult<IUpdateVulnDescriptionResultAttr>) => {
            if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
              const updateInfoSuccess: boolean = _.isUndefined(
                result.data.updateTreatmentVuln,
              )
                ? true
                : result.data.updateTreatmentVuln.success;
              const updateTreatmentSuccess: boolean = _.isUndefined(
                result.data.updateVulnsTreatment,
              )
                ? true
                : result.data.updateVulnsTreatment.success;

              return updateInfoSuccess && updateTreatmentSuccess;
            }

            return false;
          },
        );

        if (areAllMutationValid.every(Boolean)) {
          mixpanel.track("UpdatedTreatmentVulnerabilities", {
            User: (window as typeof window & { userName: string }).userName,
          });
          msgSuccess(
            translate.t(
              "search_findings.tab_description.update_vulnerabilities",
            ),
            translate.t("group_alerts.title_success"),
          );
          handleCloseModal();
        }
      } catch (updateError) {
        if (_.includes(String(updateError), "Invalid treatment manager")) {
          msgError(translate.t("group_alerts.invalid_treatment_mgr"));
        } else if (
          _.includes(
            String(updateError),
            translate.t(
              "group_alerts.organization_policies.maxium_number_of_acceptations",
            ),
          )
        ) {
          msgError(
            translate.t(
              "search_findings.tab_vuln.alerts.maximum_number_of_acceptations",
            ),
          );
        } else if (
          _.includes(
            String(updateError),
            translate.t(
              "group_alerts.organization_policies.exceeds_acceptance_date",
            ),
          )
        ) {
          msgError(
            translate.t(
              "group_alerts.organization_policies.exceeds_acceptance_date",
            ),
          );
        } else if (
          _.includes(
            String(updateError),
            translate.t(
              "group_alerts.organization_policies.exceeds_acceptance_date",
            ),
          )
        ) {
          msgError(
            translate.t(
              "group_alerts.organization_policies.exceeds_acceptance_date",
            ),
          );
        } else if (
          _.includes(
            String(updateError),
            translate.t(
              "search_findings.tab_vuln.exceptions.severity_out_of_range",
            ),
          )
        ) {
          msgError(
            translate.t(
              "group_alerts.organization_policies.severity_out_of_range",
            ),
          );
        } else {
          msgError(translate.t("group_alerts.error_textsad"));
          Logger.warning(
            "An error occurred updating vuln treatment",
            updateError,
          );
        }
      } finally {
        setRunning(false);
      }
    }
  };

  const handleEditTreatment: () => void = (): void => {
    dispatch(submit("editTreatmentVulnerability"));
  };

  const handleDeletion: (tag: string) => void = (tag: string): void => {
    deleteTagVuln({
      variables: {
        findingId: props.findingId,
        tag,
        vulnerabilities: props.vulnerabilities.map(
          (vuln: IVulnDataType) => vuln.id,
        ),
      },
    });
  };

  const [requestZeroRisk, { loading: requestingZeroRisk }] = useMutation(
    REQUEST_ZERO_RISK_VULN,
    {
      onCompleted: (
        requestZeroRiskVulnResult: IRequestZeroRiskVulnResultAttr,
      ): void => {
        if (requestZeroRiskVulnResult.requestZeroRiskVuln.success) {
          msgSuccess(
            translate.t("group_alerts.requested_zero_risk_success"),
            translate.t("group_alerts.updated_title"),
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
                error,
              );
          }
        });
      },
      refetchQueries: [
        {
          query: GET_VULNERABILITIES,
          variables: {
            analystField: canDisplayAnalyst,
            identifier: props.findingId,
          },
        },
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetExploit,
            canGetHistoricState,
            findingId: props.findingId,
          },
        },
      ],
    },
  );

  const userEmails: string[] =
    _.isUndefined(data) || _.isEmpty(data)
      ? [userEmail]
      : data.project.stakeholders.map(
          (stakeholder: Dictionary<string>): string => stakeholder.email,
        );

  const lastTreatment: IHistoricTreatment = {
    ...groupLastHistoricTreatment(props.vulnerabilities),
    justification: "",
  };

  const formValues: Dictionary<string> = useSelector((state: {}) =>
    formValueSelector("editTreatmentVulnerability")(state, "treatment", ""),
  );

  const isInProgressSelected: boolean = formValues.treatment === "IN_PROGRESS";
  const isAcceptedSelected: boolean = formValues.treatment === "ACCEPTED";
  const isAcceptedUndefinedSelected: boolean =
    formValues.treatment === "ACCEPTED_UNDEFINED";
  const isLastTreatmentAcceptanceStatusApproved: boolean =
    lastTreatment.acceptanceStatus === "APPROVED";
  const isAcceptedUndefinedPendingToApproved: boolean =
    lastTreatment.treatment === "ACCEPTED_UNDEFINED" &&
    lastTreatment.acceptanceStatus !== "APPROVED";
  const treatmentLabel: string =
    translate.t(formatDropdownField(lastTreatment.treatment)) +
    (isAcceptedUndefinedPendingToApproved
      ? translate.t(
          "search_findings.tab_description.treatment.pending_approval",
        )
      : "");

  return (
    <React.StrictMode>
      <Modal
        open={true}
        headerTitle={translate.t("search_findings.tab_description.editVuln")}
      >
        <ConfirmDialog
          message={translate.t(
            "search_findings.tab_description.approval_message",
          )}
          title={translate.t("search_findings.tab_description.approval_title")}
        >
          {(confirm: IConfirmFn): JSX.Element => {
            const handleSubmit: (values: IUpdateTreatmentVulnAttr) => void = (
              values: IUpdateTreatmentVulnAttr,
            ): void => {
              const changedToZeroRisk: boolean =
                values.treatment === "ZERO_RISK";
              const changedToUndefined: boolean =
                values.treatment === "ACCEPTED_UNDEFINED" &&
                lastTreatment.treatment !== "ACCEPTED_UNDEFINED";

              if (changedToZeroRisk) {
                void requestZeroRisk({
                  variables: {
                    findingId: props.findingId,
                    justification: values.justification,
                    vulnerabilities: props.vulnerabilities.map(
                      (vuln: IVulnDataType) => vuln.id,
                    ),
                  },
                });
              } else if (changedToUndefined) {
                confirm((): void => {
                  handleUpdateTreatmentVuln(values);
                });
              } else {
                handleUpdateTreatmentVuln(values);
              }
            };

            return (
              <React.Fragment>
                <GenericForm
                  name={"editTreatmentVulnerability"}
                  onSubmit={handleSubmit}
                  initialValues={{
                    ...lastTreatment,
                    externalBts: groupExternalBts(props.vulnerabilities),
                    severity: groupVulnLevel(props.vulnerabilities),
                    tag: _.join(_.intersection(...vulnsTags), ","),
                    treatment: lastTreatment.treatment.replace("NEW", ""),
                  }}
                >
                  <Row>
                    <Col50>
                      <EditableField
                        component={Dropdown}
                        currentValue={treatmentLabel}
                        label={translate.t(
                          "search_findings.tab_description.treatment.title",
                        )}
                        name={"treatment"}
                        renderAsEditable={
                          canUpdateVulnsTreatment || canRequestZeroRiskVuln
                        }
                        type={"text"}
                        validate={isTreatmentPristine ? [] : required}
                      >
                        <option value={""} />
                        {canUpdateVulnsTreatment ? (
                          <React.Fragment>
                            <option value={"IN_PROGRESS"}>
                              {translate.t(
                                "search_findings.tab_description.treatment.in_progress",
                              )}
                            </option>
                            <option value={"ACCEPTED"}>
                              {translate.t(
                                "search_findings.tab_description.treatment.accepted",
                              )}
                            </option>
                            <option value={"ACCEPTED_UNDEFINED"}>
                              {translate.t(
                                "search_findings.tab_description.treatment.accepted_undefined",
                              )}
                            </option>
                          </React.Fragment>
                        ) : undefined}
                        {canRequestZeroRiskVuln ? (
                          <option value={"ZERO_RISK"}>
                            {translate.t(
                              "search_findings.tab_description.treatment.zero_risk",
                            )}
                          </option>
                        ) : undefined}
                      </EditableField>
                    </Col50>
                    {isLastTreatmentAcceptanceStatusApproved ? (
                      <Col50>
                        <FormGroup>
                          <ControlLabel>
                            <b>
                              {translate.t(
                                "search_findings.tab_description.acceptation_user",
                              )}
                            </b>
                          </ControlLabel>
                          <p>{lastTreatment.user}</p>
                        </FormGroup>
                      </Col50>
                    ) : undefined}
                  </Row>
                  {isInProgressSelected ? (
                    <Row>
                      <Col50>
                        <EditableField
                          component={Dropdown}
                          currentValue={_.get(
                            lastTreatment,
                            "treatmentManager",
                            "",
                          )}
                          label={translate.t(
                            "search_findings.tab_description.treatment_mgr",
                          )}
                          name={"treatmentManager"}
                          renderAsEditable={canUpdateVulnsTreatment}
                          type={"text"}
                        >
                          <option value={""} />
                          {userEmails.map(
                            (email: string, index: number): JSX.Element => (
                              <option key={index} value={email}>
                                {email}
                              </option>
                            ),
                          )}
                        </EditableField>
                      </Col50>
                    </Row>
                  ) : undefined}
                  <Row>
                    <Col100>
                      <EditableField
                        component={TextArea}
                        currentValue={lastTreatment.justification as string}
                        label={translate.t(
                          "search_findings.tab_description.treatment_just",
                        )}
                        name={"justification"}
                        renderAsEditable={
                          canUpdateVulnsTreatment || canRequestZeroRiskVuln
                        }
                        type={"text"}
                        validate={
                          isTreatmentPristine
                            ? undefined
                            : [
                                required,
                                validTextField,
                                maxTreatmentJustificationLength,
                              ]
                        }
                      />
                    </Col100>
                  </Row>
                  {isAcceptedSelected ? (
                    <Row>
                      <Col50>
                        <EditableField
                          component={Date}
                          currentValue={_.get(
                            lastTreatment,
                            "acceptanceDate",
                            "-",
                          )}
                          label={translate.t(
                            "search_findings.tab_description.acceptance_date",
                          )}
                          name={"acceptanceDate"}
                          renderAsEditable={canUpdateVulnsTreatment}
                          type={"date"}
                          validate={[required, isLowerDate]}
                        />
                      </Col50>
                    </Row>
                  ) : undefined}
                  {isInProgressSelected ||
                  isAcceptedSelected ||
                  isAcceptedUndefinedSelected ? (
                    <React.Fragment>
                      <Row>
                        <Col100>
                          <EditableField
                            component={Text}
                            currentValue={groupExternalBts(
                              props.vulnerabilities,
                            )}
                            label={translate.t(
                              "search_findings.tab_description.bts",
                            )}
                            name={"externalBts"}
                            placeholder={translate.t(
                              "search_findings.tab_description.bts_placeholder",
                            )}
                            renderAsEditable={canUpdateVulnsTreatment}
                            type={"text"}
                            validate={[maxBtsLength, validUrlField]}
                          />
                        </Col100>
                      </Row>
                      <Row>
                        <Col100>
                          <FormGroup>
                            <ControlLabel>
                              <b>
                                {translate.t(
                                  "search_findings.tab_description.tag",
                                )}
                              </b>
                            </ControlLabel>
                            <Field
                              component={TagInput}
                              name={"tag"}
                              onDeletion={handleDeletion}
                              type={"text"}
                            />
                          </FormGroup>
                        </Col100>
                        <Col50>
                          <FormGroup>
                            <ControlLabel>
                              <b>
                                {translate.t(
                                  "search_findings.tab_description.business_criticality",
                                )}
                              </b>
                            </ControlLabel>
                            <Field
                              component={Text}
                              name={"severity"}
                              type={"number"}
                              validate={[isValidVulnSeverity, numeric]}
                            />
                          </FormGroup>
                        </Col50>
                      </Row>
                    </React.Fragment>
                  ) : undefined}
                </GenericForm>
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
              </React.Fragment>
            );
          }}
        </ConfirmDialog>
      </Modal>
    </React.StrictMode>
  );
};

export { updateTreatmentModal as UpdateTreatmentModal };
