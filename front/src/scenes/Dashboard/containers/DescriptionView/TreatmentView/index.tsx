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
}

const treatmentView: React.FC<ITreatmentViewProps> = (props: ITreatmentViewProps): JSX.Element => {
  // State management
  const selector: (state: {}, ...field: string[]) => Dictionary<string> = formValueSelector("editTreatment");
  const formValues: Dictionary<string> = useSelector((state: {}) => selector(state, "treatment", ""));

  // GraphQL operations
  const { data, refetch } = useQuery(GET_FINDING_TREATMENT, {
    variables: { findingId: props.findingId },
  });

  const canEditTreatment: boolean = _.includes(["admin", "customer", "customeradmin"], props.userRole);

  const [updateTreatment] = useMutation(UPDATE_TREATMENT_MUTATION, {
    onCompleted: async (result: { updateDescription: { success: boolean } }): Promise<void> => {
      if (result.updateDescription.success) {
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
    await updateTreatment({ variables: { ...values, findingId: props.findingId } });
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
    <GenericForm
      name="editTreatment"
      initialValues={{ ...lastTreatment, btsUrl: data.finding.btsUrl }}
      onSubmit={handleSubmit}
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
              currentValue={lastTreatment.acceptanceDate as string}
              label={translate.t("search_findings.tab_description.acceptance_date")}
              name="acceptanceDate"
              renderAsEditable={props.isEditing}
              type="date"
              validate={[isValidDate, isLowerDate]}
              visibleWhileEditing={canEditTreatment}
            />
          </Col>
        </Row>
      ) : undefined}
    </GenericForm>
  );
};

export { treatmentView as TreatmentView };
