/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props and
 * conditional rendering
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { useSelector } from "react-redux";
import { formValueSelector } from "redux-form";
import { ConfirmDialog, ConfirmFn } from "../../../../../components/ConfirmDialog";
import { formatDropdownField, getLastTreatment } from "../../../../../utils/formatHelpers";
import { dateField, dropdownField, textAreaField, textField } from "../../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import rollbar from "../../../../../utils/rollbar";
import translate from "../../../../../utils/translations/translate";
import { isLowerDate, isValidDate, required } from "../../../../../utils/validations";
import { EditableField } from "../../../components/EditableField";
import { GenericForm } from "../../../components/GenericForm";
import { IHistoricTreatment } from "../types";
import { GET_FINDING_TREATMENT, UPDATE_TREATMENT_MUTATION } from "./queries";

interface ITreatmentViewProps {
  findingId: string;
  isEditing: boolean;
  userRole: string;
  setEditing(value: boolean): void;
}

const treatmentView: React.FC<ITreatmentViewProps> = (props: ITreatmentViewProps): JSX.Element => {
  // State management
  const formValues: Dictionary<string> = useSelector((state: {}) =>
    formValueSelector("editTreatment")(state, "treatment", ""));

  // GraphQL operations
  const { data, refetch } = useQuery(GET_FINDING_TREATMENT, {
    variables: { findingId: props.findingId },
  });

  const canEditTreatment: boolean = _.includes(["customer", "customeradmin"], props.userRole);

  const [updateTreatment] = useMutation(UPDATE_TREATMENT_MUTATION, {
    onCompleted: async (result: { updateClientDescription: { success: boolean } }): Promise<void> => {
      if (result.updateClientDescription.success) {
        msgSuccess(
          translate.t("proj_alerts.updated"),
          translate.t("proj_alerts.updated_title"),
        );
        await refetch();
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Invalid treatment manager":
            msgError(translate.t("proj_alerts.invalid_treatment_mgr"));
            break;
          case "Exception - The inserted date is invalid":
            msgError(translate.t("proj_alerts.invalid_date"));
            break;
          default:
            msgError(translate.t("proj_alerts.error_textsad"));
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

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const lastTreatment: IHistoricTreatment = getLastTreatment(data.finding.historicTreatment);

  let treatmentLabel: string = translate.t(formatDropdownField(formValues.treatment));
  if (formValues.treatment === "ACCEPTED_UNDEFINED" && lastTreatment.acceptanceStatus !== "APPROVED") {
    treatmentLabel += translate.t("search_findings.tab_description.treatment.pending_approval");
  }

  return (
    <ConfirmDialog
      message={translate.t("search_findings.tab_description.approval_message")}
      title={translate.t("search_findings.tab_description.approval_title")}
    >
      {(confirm: ConfirmFn): JSX.Element => {
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
      initialValues={{ ...lastTreatment, btsUrl: data.finding.btsUrl }}
      onSubmit={confirmUndefined}
    >
      <Row>
        <Col md={12}>
          <EditableField
            component={textField}
            currentValue={data.finding.btsUrl}
            label={translate.t("search_findings.tab_description.bts")}
            name="btsUrl"
            renderAsEditable={props.isEditing}
            type="text"
            validate={required}
            visibleWhileEditing={canEditTreatment}
          />
        </Col>
      </Row>
      <Row>
        <Col md={6}>
          <EditableField
            component={dropdownField}
            currentValue={treatmentLabel}
            label={translate.t("search_findings.tab_description.treatment.title")}
            name="treatment"
            renderAsEditable={props.isEditing}
            type="text"
            validate={required}
            visibleWhileEditing={canEditTreatment}
          >
            <option value="" />
            <option value="IN PROGRESS">
              {translate.t("search_findings.tab_description.treatment.in_progress")}
            </option>
            <option value="ACCEPTED">
              {translate.t("search_findings.tab_description.treatment.accepted")}
            </option>
            <option value="ACCEPTED_UNDEFINED">
              {translate.t("search_findings.tab_description.treatment.accepted_undefined")}
            </option>
          </EditableField>
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
          <EditableField
            component={textAreaField}
            currentValue={lastTreatment.justification as string}
            label={translate.t("search_findings.tab_description.treatment_just")}
            name="justification"
            renderAsEditable={props.isEditing}
            type="text"
            validate={[required]}
            visibleWhileEditing={canEditTreatment}
          />
        </Col>
      </Row>
      {formValues.treatment === "ACCEPTED" ? (
        <Row>
          <Col md={4}>
            <EditableField
              component={dateField}
              currentValue={_.get(lastTreatment, "acceptanceDate", "-")}
              label={translate.t("search_findings.tab_description.acceptance_date")}
              name="date"
              renderAsEditable={props.isEditing}
              type="date"
              validate={[required, isValidDate, isLowerDate]}
              visibleWhileEditing={canEditTreatment}
            />
          </Col>
        </Row>
      ) : undefined}
    </GenericForm>
        );
      }}
    </ConfirmDialog>
  );
};

export { treatmentView as TreatmentView };
