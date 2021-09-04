import { Field, Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import type { ConfigurableValidator } from "revalidate";

import { TooltipWrapper } from "components/TooltipWrapper";
import { ActionButtons } from "scenes/Dashboard/containers/DescriptionView/ActionButtons";
import type {
  IFinding,
  IFindingDescriptionData,
} from "scenes/Dashboard/containers/DescriptionView/types";
import {
  Col100,
  Col45,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import {
  EditableField,
  FormikDropdown,
  FormikText,
  FormikTextArea,
} from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  maxLength,
  required,
  validDraftTitle,
  validTextField,
} from "utils/validations";

const MAX_TITLE_LENGTH = 90;
const MAX_DESCRIPTION_LENGTH = 500;
const MAX_REQUIREMENTS_LENGTH = 500;
const MAX_IMPACTS_LENGTH = 300;
const MAX_AFFECTED_SYSTEMS_LENGTH = 200;
const MAX_THREAT_LENGTH = 300;
const MAX_RECOMENDATION_LENGTH = 300;
const maxTitleLength: ConfigurableValidator = maxLength(MAX_TITLE_LENGTH);
const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);
const maxRequirementsLength: ConfigurableValidator = maxLength(
  MAX_REQUIREMENTS_LENGTH
);
const maxImpactsLength: ConfigurableValidator = maxLength(MAX_IMPACTS_LENGTH);
const maxAffectedSystemsLength: ConfigurableValidator = maxLength(
  MAX_AFFECTED_SYSTEMS_LENGTH
);
const maxThreatLength: ConfigurableValidator = maxLength(MAX_THREAT_LENGTH);
const maxRecommendationLength: ConfigurableValidator = maxLength(
  MAX_RECOMENDATION_LENGTH
);

interface IDescriptionViewFormProps {
  data: IFindingDescriptionData | undefined;
  isEditing: boolean;
  setEditing: React.Dispatch<React.SetStateAction<boolean>>;
}

const DescriptionViewForm: React.FC<IDescriptionViewFormProps> = ({
  data,
  isEditing,
  setEditing,
}: IDescriptionViewFormProps): JSX.Element => {
  const { dirty, resetForm, submitForm } = useFormikContext();

  const isDescriptionPristine = !dirty;

  const toggleEdit: () => void = useCallback((): void => {
    if (!isDescriptionPristine) {
      resetForm();
    }
    setEditing(!isEditing);
  }, [isDescriptionPristine, isEditing, resetForm, setEditing]);

  const handleSubmit: () => void = useCallback((): void => {
    if (!isDescriptionPristine) {
      void submitForm();
    }
  }, [isDescriptionPristine, submitForm]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset: IFinding = data.finding;

  return (
    <Form id={"editDescription"}>
      <ActionButtons
        isEditing={isEditing}
        isPristine={isDescriptionPristine}
        onEdit={toggleEdit}
        onUpdate={handleSubmit}
      />
      <br />
      <div>
        <div>
          <Row>
            <Can do={"api_resolvers_finding_hacker_resolve"}>
              <Col45>
                <FormGroup>
                  <ControlLabel>
                    <b>{translate.t("searchFindings.tabDescription.hacker")}</b>
                  </ControlLabel>
                  <p className={"ma0"}>{dataset.hacker}</p>
                </FormGroup>
              </Col45>
            </Can>
          </Row>
          <Can do={"api_mutations_update_finding_description_mutate"}>
            {isEditing ? (
              <Row>
                <Col100>
                  <TooltipWrapper
                    id={"searchFindings.tabDescription.title.tooltip"}
                    message={translate.t(
                      "searchFindings.tabDescription.title.tooltip"
                    )}
                  >
                    <FormGroup>
                      <ControlLabel>
                        <b>
                          {translate.t(
                            "searchFindings.tabDescription.title.text"
                          )}
                        </b>
                      </ControlLabel>
                      <br />
                      <Field
                        component={FormikText}
                        name={"title"}
                        type={"text"}
                        validate={composeValidators([
                          required,
                          validDraftTitle,
                          validTextField,
                          maxTitleLength,
                        ])}
                      />
                    </FormGroup>
                  </TooltipWrapper>
                </Col100>
              </Row>
            ) : undefined}
          </Can>
          <Row>
            <Col100>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.description}
                    id={"searchFindings.tabDescription.description.tooltip"}
                    label={translate.t(
                      "searchFindings.tabDescription.description.text"
                    )}
                    name={"description"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.description.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxDescriptionLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col100>
          </Row>
          <Row>
            <Col100>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.requirements}
                    id={"searchFindings.tabDescription.requirements.tooltip"}
                    label={translate.t(
                      "searchFindings.tabDescription.requirements.text"
                    )}
                    name={"requirements"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.requirements.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxRequirementsLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col100>
          </Row>
          <Row>
            <Col45>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.attackVectorDescription}
                    id={"searchFindings.tabDescription.attackVectors.tooltip"}
                    label={translate.t(
                      "searchFindings.tabDescription.attackVectors.text"
                    )}
                    name={"attackVectorDescription"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.attackVectors.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxImpactsLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col45>
            <Col45>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.affectedSystems}
                    id={"searchFindings.tabDescription.affectedSystems.tooltip"}
                    label={translate.t(
                      "searchFindings.tabDescription.affectedSystems.text"
                    )}
                    name={"affectedSystems"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.affectedSystems.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxAffectedSystemsLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col45>
          </Row>
          <Row>
            <Col45>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.threat}
                    id={"searchFindings.tabDescription.threat.tooltip"}
                    label={translate.t(
                      "searchFindings.tabDescription.threat.text"
                    )}
                    name={"threat"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.threat.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxThreatLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col45>
          </Row>
          <Row>
            <Col100>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.recommendation}
                    id={"searchFindings.tabDescription.recommendation.tooltip"}
                    label={translate.t(
                      "searchFindings.tabDescription.recommendation.text"
                    )}
                    name={"recommendation"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.recommendation.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxRecommendationLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col100>
          </Row>
          <Can do={"api_mutations_update_finding_description_mutate"}>
            {isEditing ? (
              <Row>
                <Col45>
                  <TooltipWrapper
                    id={"searchFindings.tabDescription.sorts.tooltip"}
                    message={translate.t(
                      "searchFindings.tabDescription.sorts.tooltip"
                    )}
                  >
                    <FormGroup>
                      <ControlLabel>
                        <b>
                          {translate.t(
                            "searchFindings.tabDescription.sorts.text"
                          )}
                        </b>
                      </ControlLabel>
                      <br />
                      <Field
                        component={FormikDropdown}
                        name={"sorts"}
                        type={"text"}
                        validate={composeValidators([required])}
                      >
                        <option value={""} />
                        <option value={"NO"}>
                          {translate.t("group.findings.boolean.False")}
                        </option>
                        <option value={"YES"}>
                          {translate.t("group.findings.boolean.True")}
                        </option>
                      </Field>
                    </FormGroup>
                  </TooltipWrapper>
                </Col45>
              </Row>
            ) : undefined}
          </Can>
        </div>
      </div>
    </Form>
  );
};

export { DescriptionViewForm };
