/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props and
 * conditional rendering
 */

import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";
import { formatCweUrl, formatFindingType } from "../../../../utils/formatHelpers";
import { dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { numeric, required, validDraftTitle } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { GenericForm } from "../../components/GenericForm";
import { GET_ROLE } from "../ProjectContent/queries";
import { GET_FINDING_DESCRIPTION, UPDATE_DESCRIPTION_MUTATION } from "./queries";
import { TreatmentView } from "./TreatmentView";
import { IFinding } from "./types";

type DescriptionViewProps = RouteComponentProps<{ findingId: string; projectName: string }>;

const descriptionView: React.FC<DescriptionViewProps> = (props: DescriptionViewProps): JSX.Element => {
  const { findingId, projectName } = props.match.params;
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingDescription", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const [isEditing, setEditing] = React.useState(false);
  const toggleEdit: (() => void) = (): void => { setEditing(!isEditing); };

  // GraphQL operations
  const { data: userData } = useQuery(GET_ROLE, { variables: { projectName } });
  const userRole: string = _.isUndefined(userData) || _.isEmpty(userData)
    ? "" : userData.me.role;

  const canEditAffectedSystems: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditCompromisedAttrs: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditCompromisedRecords: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditDescription: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditImpact: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditThreat: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditTitle: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditType: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditRecommendation: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditRequirements: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditWeakness: boolean = _.includes(["admin", "analyst"], userRole);
  const canRetrieveAnalyst: boolean = _.includes(["admin", "analyst"], userRole);

  const { data, refetch } = useQuery(GET_FINDING_DESCRIPTION, {
    skip: _.isEmpty(userRole),
    variables: {
      canRetrieveAnalyst,
      findingId,
      projectName,
    },
  });

  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION, {
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
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred updating finding description", updateError);
    },
  });

  const handleSubmit: ((values: Dictionary<string>) => Promise<void>) = async (
    values: Dictionary<string>,
  ): Promise<void> => {
    setEditing(false);
    await updateDescription({ variables: { ...values, findingId } });
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const dataset: IFinding = data.finding;

  return (
    <React.StrictMode>
      <GenericForm name="editDescription" initialValues={dataset} onSubmit={handleSubmit}>
        {({ pristine }: InjectedFormProps): React.ReactNode => (
          <React.Fragment>
            <Row>
              <ButtonToolbar className="pull-right">
                {isEditing ? (
                  <Button type="submit" disabled={pristine}>
                    <FluidIcon icon="loading" /> {translate.t("search_findings.tab_description.update")}
                  </Button>
                ) : undefined}
                <Button onClick={toggleEdit}>
                  <FluidIcon icon="edit" /> {translate.t("search_findings.tab_description.editable")}
                </Button>
              </ButtonToolbar>
            </Row>
            <Row>
              <Col md={6}>
                <EditableField
                  component={dropdownField}
                  currentValue={formatFindingType(dataset.type)}
                  label={translate.t("search_findings.tab_description.type.title")}
                  name="type"
                  renderAsEditable={isEditing}
                  validate={[required]}
                  visibleWhileEditing={canEditType}
                >
                  <option value="" />
                  <option value="SECURITY">{translate.t("search_findings.tab_description.type.security")}</option>
                  <option value="HYGIENE">{translate.t("search_findings.tab_description.type.hygiene")}</option>
                </EditableField>
              </Col>
              {canRetrieveAnalyst ? (
                <Col md={6}>
                  <FormGroup>
                    <ControlLabel>
                      <b>{translate.t("search_findings.tab_description.analyst")}</b>
                    </ControlLabel>
                    <p>{dataset.analyst}</p>
                  </FormGroup>
                </Col>
              ) : undefined}
            </Row>
            {isEditing && canEditTitle ? (
              <Row>
                <Col md={12}>
                  <FormGroup>
                    <ControlLabel>
                      <b>{translate.t("search_findings.tab_description.title")}</b>
                    </ControlLabel>
                    <br />
                    <Field
                      component={textField}
                      name="title"
                      type="text"
                      validate={[required, validDraftTitle]}
                    />
                  </FormGroup>
                </Col>
              </Row>
            ) : undefined}
            <Row>
              <Col md={12}>
                <EditableField
                  component={textAreaField}
                  currentValue={dataset.description}
                  label={translate.t("search_findings.tab_description.description")}
                  name="description"
                  renderAsEditable={isEditing}
                  type="text"
                  validate={[required]}
                  visibleWhileEditing={canEditDescription}
                />
              </Col>
            </Row>
            <Row>
              <Col md={12}>
                <EditableField
                  component={textAreaField}
                  currentValue={dataset.requirements}
                  label={translate.t("search_findings.tab_description.requirements")}
                  name="requirements"
                  renderAsEditable={isEditing}
                  type="text"
                  validate={[required]}
                  visibleWhileEditing={canEditRequirements}
                />
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <EditableField
                  component={textAreaField}
                  currentValue={dataset.attackVectorDesc}
                  label={translate.t("search_findings.tab_description.attack_vectors")}
                  name="attackVectorDesc"
                  renderAsEditable={isEditing}
                  type="text"
                  validate={[required]}
                  visibleWhileEditing={canEditImpact}
                />
              </Col>
              <Col md={6}>
                <EditableField
                  component={textAreaField}
                  currentValue={dataset.affectedSystems}
                  label={translate.t("search_findings.tab_description.affected_systems")}
                  name="affectedSystems"
                  renderAsEditable={isEditing}
                  type="text"
                  validate={[required]}
                  visibleWhileEditing={canEditAffectedSystems}
                />
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <EditableField
                  component={textAreaField}
                  currentValue={dataset.threat}
                  label={translate.t("search_findings.tab_description.threat")}
                  name="threat"
                  renderAsEditable={isEditing}
                  type="text"
                  validate={[required]}
                  visibleWhileEditing={canEditThreat}
                />
              </Col>
              <Col md={6}>
                <EditableField
                  component={textField}
                  currentValue={formatCweUrl(dataset.cweUrl)}
                  label={translate.t("search_findings.tab_description.weakness")}
                  name="cweUrl"
                  renderAsEditable={isEditing}
                  type="number"
                  validate={[required, numeric]}
                  visibleWhileEditing={canEditWeakness}
                />
              </Col>
            </Row>
            <Row>
              <Col md={12}>
                <EditableField
                  component={textAreaField}
                  currentValue={dataset.recommendation}
                  label={translate.t("search_findings.tab_description.recommendation")}
                  name="recommendation"
                  renderAsEditable={isEditing}
                  type="text"
                  validate={[required]}
                  visibleWhileEditing={canEditRecommendation}
                />
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <EditableField
                  component={textAreaField}
                  currentValue={dataset.compromisedAttributes}
                  label={translate.t("search_findings.tab_description.compromised_attrs")}
                  name="compromisedAttributes"
                  renderAsEditable={isEditing}
                  type="text"
                  visibleWhileEditing={canEditCompromisedAttrs}
                />
              </Col>
              <Col md={6}>
                <EditableField
                  component={textAreaField}
                  currentValue={dataset.compromisedRecords}
                  label={translate.t("search_findings.tab_description.compromised_records")}
                  name="compromisedRecords"
                  renderAsEditable={isEditing}
                  type="number"
                  validate={[required, numeric]}
                  visibleWhileEditing={canEditCompromisedRecords}
                />
              </Col>
            </Row>
            <TreatmentView findingId={findingId} isEditing={isEditing} userRole={userRole} />
          </React.Fragment>
        )}
      </GenericForm>
    </React.StrictMode>
  );
};

export { descriptionView as DescriptionView };
