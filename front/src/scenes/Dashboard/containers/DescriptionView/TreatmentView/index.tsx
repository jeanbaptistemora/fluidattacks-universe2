/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props and
 * conditional rendering
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { useSelector } from "react-redux";
import { formValueSelector } from "redux-form";
import { ConfigurableValidator } from "revalidate";
import { ConfirmDialog, IConfirmFn } from "../../../../../components/ConfirmDialog";
import { DataTableNext } from "../../../../../components/DataTableNext";
import { IHeaderConfig } from "../../../../../components/DataTableNext/types";
import { FluidIcon } from "../../../../../components/FluidIcon";
import { Can } from "../../../../../utils/authz/Can";
import { formatDropdownField, getLastTreatment, getPreviousTreatment } from "../../../../../utils/formatHelpers";
import { dateField, Dropdown, Text, TextArea } from "../../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import rollbar from "../../../../../utils/rollbar";
import translate from "../../../../../utils/translations/translate";
import {
  isLowerDate, maxLength, required, validTextField, validUrlField,
} from "../../../../../utils/validations";
import { EditableField } from "../../../components/EditableField";
import { GenericForm } from "../../../components/GenericForm";
import { RemediationModal } from "../../../components/RemediationModal";
import { HANDLE_ACCEPTATION } from "../queries";
import { IHistoricTreatment } from "../types";
import { default as style } from "./index.css";
import { GET_FINDING_TREATMENT, UPDATE_TREATMENT_MUTATION } from "./queries";

export interface ITreatmentViewProps {
  approvalModalConfig: { open: boolean; type: string };
  findingId: string;
  isEditing: boolean;
  projectName: string;
  onCloseApproval(): void;
  setEditing(value: boolean): void;
}

const maxBtsLength: ConfigurableValidator = maxLength(80);
const maxTreatmentJustificationLength: ConfigurableValidator = maxLength(200);
const treatmentView: React.FC<ITreatmentViewProps> = (props: ITreatmentViewProps): JSX.Element => {
  const { onCloseApproval } = props;
  const { userName } = window as typeof window & Dictionary<string>;

  // State management
  const formValues: Dictionary<string> = useSelector((state: {}) =>
    formValueSelector("editTreatment")(state, "treatment", ""));
  const [isTreatmentExpanded, toggleTreatmentExpansion] = React.useState(false);

  const expandHistoricTreatment: (() => void) = (): void => {
    toggleTreatmentExpansion(!isTreatmentExpanded);
  };

  // GraphQL operations
  const { data, refetch } = useQuery(GET_FINDING_TREATMENT, {
    variables: { findingId: props.findingId },
  });

  const [updateTreatment] = useMutation(UPDATE_TREATMENT_MUTATION, {
    onCompleted: async (result: { updateClientDescription: { success: boolean } }): Promise<void> => {
      if (result.updateClientDescription.success) {
        msgSuccess(
          translate.t("group_alerts.updated"),
          translate.t("group_alerts.updated_title"),
        );
        await refetch();
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Finding treatment cannot be updated with the same values":
            break;
          case "Invalid treatment manager":
            msgError(translate.t("group_alerts.invalid_treatment_mgr"));
            break;
          case "Exception - The inserted date is invalid":
            msgError(translate.t("group_alerts.invalid_date"));
            break;
          case "Exception - Invalid field in form":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - Invalid characters":
            msgError(translate.t("validations.invalid_char"));
            break;
          case "Exception - Chosen date is either in the past or exceeds the maximum number of days " +
              "allowed by the organization":
            msgError(translate.t("group_alerts.organization_policies.exceeds_acceptance_date"));
            break;
          case "Exception - Finding cannot be accepted, severity outside of range set by the organization":
            msgError(translate.t("group_alerts.organization_policies.severity_out_of_range"));
            break;
          case "Exception - Finding has been accepted the maximum number of times allowed by the organization":
            msgError(translate.t("group_alerts.organization_policies.maxium_number_of_acceptations"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            rollbar.error("An error occurred updating treatment", updateError);
        }
      });
    },
  });

  const handleSubmit: ((values: Dictionary<string>) => void) = async (
    values: Dictionary<string>,
  ): Promise<void> => {
    props.setEditing(false);
    await updateTreatment({
      variables: {
        ...values,
        acceptanceStatus: values.treatment === "ACCEPTED_UNDEFINED" ? "SUBMITTED" : "",
        findingId: props.findingId,
      },
    });
  };

  const [handleAcceptation, { loading: approving }] = useMutation(HANDLE_ACCEPTATION, {
    onCompleted: async (result: { handleAcceptation: { success: boolean } }): Promise<void> => {
      if (result.handleAcceptation.success) {
        mixpanel.track("HandleAcceptation", { User: userName });
        await refetch();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred approving acceptation", error);
      });
    },
  });

  const handleApprovalSubmit: ((values: Dictionary<string>) => void) = async (
    values: Dictionary<string>,
  ): Promise<void> => {
    await handleAcceptation({
      variables: {
        findingId: props.findingId,
        observations: values.treatmentJustification,
        projectName: props.projectName,
        response: props.approvalModalConfig.type,
      },
    });
    props.onCloseApproval();
    msgSuccess(
      props.approvalModalConfig.type === "APPROVED"
        ? translate.t("group_alerts.acceptation_approved")
        : translate.t("group_alerts.acceptation_rejected"),
      translate.t("group_alerts.updated_title"),
    );
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const lastTreatment: IHistoricTreatment = getLastTreatment(data.finding.historicTreatment);
  const historicTreatment: IHistoricTreatment[] = getPreviousTreatment(data.finding.historicTreatment);
  const historicTreatmentHeaders: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "date",
      header: translate.t("search_findings.tab_description.treatment_date"),
    },
    {
      align: "center",
      dataField: "treatment",
      header: translate.t("search_findings.tab_description.treatment.title"),
    },
    {
      align: "center",
      dataField: "acceptanceDate",
      header: translate.t("search_findings.tab_description.acceptance_date"),
    },
    {
      align: "left",
      dataField: "justification",
      header: translate.t("search_findings.tab_description.treatment_just"),
    },
    {
      align: "center",
      dataField: "user",
      header: translate.t("search_findings.tab_description.treatment_mgr"),
    }];

  let treatmentLabel: string = translate.t(formatDropdownField(lastTreatment.treatment));
  if (lastTreatment.treatment === "ACCEPTED_UNDEFINED" && lastTreatment.acceptanceStatus !== "APPROVED") {
    treatmentLabel += translate.t("search_findings.tab_description.treatment.pending_approval");
  }

  return (
    <React.StrictMode>
      <ConfirmDialog
        message={translate.t("search_findings.tab_description.approval_message")}
        title={translate.t("search_findings.tab_description.approval_title")}
      >
        {(confirm: IConfirmFn): JSX.Element => {
          const confirmUndefined: ((values: Dictionary<string>) => void) = (values: Dictionary<string>): void => {
            const changedToUndefined: boolean =
              values.treatment === "ACCEPTED_UNDEFINED"
              && lastTreatment.treatment !== "ACCEPTED_UNDEFINED";

            if (changedToUndefined) {
              confirm((): void => { handleSubmit(values); });
            } else {
              handleSubmit(values);
            }
          };

          return (
            <GenericForm
              name="editTreatment"
              initialValues={{
                ...lastTreatment,
                btsUrl: data.finding.btsUrl,
                treatment: lastTreatment.treatment.replace("NEW", ""),
              }}
              onSubmit={confirmUndefined}
            >
              <Row>
                <Col md={12}>
                  <Can do="backend_api_resolvers_finding__do_update_client_description" passThrough={true}>
                    {(canEdit: boolean): JSX.Element => (
                      <EditableField
                        component={Text}
                        currentValue={data.finding.btsUrl}
                        label={translate.t("search_findings.tab_description.bts")}
                        name="btsUrl"
                        placeholder={translate.t("search_findings.tab_description.bts_placeholder")}
                        renderAsEditable={props.isEditing}
                        type="text"
                        visibleWhileEditing={canEdit}
                        validate={[validUrlField, maxBtsLength]}
                      />
                    )}
                  </Can>
                </Col>
              </Row>
              <Row>
                <Col md={6}>
                  <Can do="backend_api_resolvers_finding__do_update_client_description" passThrough={true}>
                    {(canEdit: boolean): JSX.Element => (
                      <EditableField
                        component={Dropdown}
                        currentValue={treatmentLabel}
                        label={translate.t("search_findings.tab_description.treatment.title")}
                        name="treatment"
                        renderAsEditable={props.isEditing}
                        type="text"
                        validate={required}
                        visibleWhileEditing={canEdit}
                      >
                        <option value="" />
                        <option value="IN_PROGRESS">
                          {translate.t("search_findings.tab_description.treatment.in_progress")}
                        </option>
                        <option value="ACCEPTED">
                          {translate.t("search_findings.tab_description.treatment.accepted")}
                        </option>
                        <option value="ACCEPTED_UNDEFINED">
                          {translate.t("search_findings.tab_description.treatment.accepted_undefined")}
                        </option>
                      </EditableField>
                    )}
                  </Can>
                </Col>
                {lastTreatment.acceptanceStatus === "APPROVED" ? (
                  <Col md={6}>
                    <FormGroup>
                      <ControlLabel>
                        <b>{translate.t("search_findings.tab_description.acceptation_user")}</b>
                      </ControlLabel>
                      <p>{lastTreatment.user}</p>
                    </FormGroup>
                  </Col>
                ) : undefined}
              </Row>
              <Row>
                <Col md={12}>
                  <Can do="backend_api_resolvers_finding__do_update_client_description" passThrough={true}>
                    {(canEdit: boolean): JSX.Element => (
                      <EditableField
                        component={TextArea}
                        currentValue={lastTreatment.justification as string}
                        label={translate.t("search_findings.tab_description.treatment_just")}
                        name="justification"
                        renderAsEditable={props.isEditing}
                        type="text"
                        validate={[required, validTextField, maxTreatmentJustificationLength]}
                        visibleWhileEditing={canEdit}
                      />
                    )}
                  </Can>
                </Col>
              </Row>
              {formValues.treatment === "ACCEPTED" ? (
                <Row>
                  <Col md={4}>
                    <Can do="backend_api_resolvers_finding__do_update_client_description" passThrough={true}>
                      {(canEdit: boolean): JSX.Element => (
                        <EditableField
                          component={dateField}
                          currentValue={_.get(lastTreatment, "acceptanceDate", "-")}
                          label={translate.t("search_findings.tab_description.acceptance_date")}
                          name="date"
                          renderAsEditable={props.isEditing}
                          type="date"
                          validate={[required, isLowerDate]}
                          visibleWhileEditing={canEdit}
                        />
                      )}
                    </Can>
                  </Col>
                </Row>
              ) : undefined}
              {!_.isEmpty(historicTreatment) && !props.isEditing ? (
                <Row>
                  <Col md={12}>
                    {isTreatmentExpanded ? (
                      <React.Fragment>
                        <label className={style.historicTreatment} onClick={expandHistoricTreatment}>
                          <FluidIcon icon="caretDown" />
                            &nbsp; {translate.t("search_findings.tab_description.treatment_historic")}
                        </label>
                        <DataTableNext
                          id="historicTreatment"
                          bordered={false}
                          dataset={historicTreatment}
                          exportCsv={false}
                          headers={historicTreatmentHeaders}
                          pageSize={5}
                          search={false}
                          tableHeader={style.tableHeader}
                          tableBody={style.tableBody}
                        />
                      </React.Fragment>
                    ) :
                      <React.Fragment>
                        <label className={style.historicTreatment} onClick={expandHistoricTreatment}>
                          <FluidIcon icon="caretRight" />
                            &nbsp; {translate.t("search_findings.tab_description.treatment_historic")}
                        </label>
                      </React.Fragment>}
                  </Col>
                </Row>
              ) : undefined}
            </GenericForm>
          );
        }}
      </ConfirmDialog>
      <RemediationModal
        additionalInfo={
          props.approvalModalConfig.type === "APPROVED"
            ? `${data.finding.openVulnerabilities} vulnerabilities will be assumed`
            : undefined
        }
        isLoading={approving}
        isOpen={props.approvalModalConfig.open}
        message={translate.t("search_findings.tab_description.remediation_modal.observations")}
        onClose={onCloseApproval}
        onSubmit={handleApprovalSubmit}
        title={translate.t("search_findings.tab_description.remediation_modal.title_observations")}
      />
    </React.StrictMode>
  );
};

export { treatmentView as TreatmentView };
