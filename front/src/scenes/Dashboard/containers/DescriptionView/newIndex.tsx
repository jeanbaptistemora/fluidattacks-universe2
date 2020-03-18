/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props and
 * conditional rendering
 */

import { useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";
import { formatFindingDescription, formatFindingType } from "../../../../utils/formatHelpers";
import { dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required, validDraftTitle } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { GenericForm } from "../../components/GenericForm";
import { GET_ROLE } from "../ProjectContent/queries";
import { GET_FINDING_DESCRIPTION } from "./queries";
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

  const canEditDescription: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditTitle: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditTreatmentMgr: boolean = _.includes(["admin", "customeradmin"], userRole);
  const canEditType: boolean = _.includes(["admin", "analyst"], userRole);
  const canEditRequirements: boolean = _.includes(["admin", "analyst"], userRole);
  const canRetrieveAnalyst: boolean = _.includes(["admin", "analyst"], userRole);

  const { data } = useQuery(GET_FINDING_DESCRIPTION, {
    skip: _.isEmpty(userRole),
    variables: {
      canEditTreatmentMgr,
      canRetrieveAnalyst,
      findingId,
      projectName,
    },
  });

  const handleSubmit: ((values: Dictionary<string>) => void) = (): void => undefined;

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const dataset: IFinding = formatFindingDescription(data.finding);

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
                  visible={!isEditing || (isEditing && canEditType)}
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
            <Row>
              <Col md={12}>
                <EditableField
                  component={textField}
                  currentValue=""
                  label={translate.t("search_findings.tab_description.title")}
                  name="title"
                  renderAsEditable={true}
                  type="text"
                  validate={[required, validDraftTitle]}
                  visible={isEditing && canEditTitle}
                />
              </Col>
            </Row>
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
                  visible={!isEditing || (isEditing && canEditDescription)}
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
                  visible={!isEditing || (isEditing && canEditRequirements)}
                />
              </Col>
            </Row>
          </React.Fragment>
        )}
      </GenericForm>
    </React.StrictMode>
  );
};

export { descriptionView as DescriptionView };
