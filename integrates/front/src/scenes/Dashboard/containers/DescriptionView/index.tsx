import { useMutation, useQuery } from "@apollo/react-hooks";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { ApolloError } from "apollo-client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router";
import type { Dispatch } from "redux";
import { Field, isPristine, reset, submit } from "redux-form";
import type { ConfigurableValidator } from "revalidate";

import { TooltipWrapper } from "components/TooltipWrapper";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { ActionButtons } from "scenes/Dashboard/containers/DescriptionView/ActionButtons";
import {
  GET_FINDING_DESCRIPTION,
  UPDATE_DESCRIPTION_MUTATION,
} from "scenes/Dashboard/containers/DescriptionView/queries";
import type {
  IFinding,
  IFindingDescriptionData,
  IFindingDescriptionVars,
} from "scenes/Dashboard/containers/DescriptionView/types";
import {
  formatCompromisedRecords,
  formatCweUrl,
  formatFindingType,
} from "scenes/Dashboard/containers/DescriptionView/utils";
import {
  Col100,
  Col45,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Dropdown, Text, TextArea } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  maxLength,
  numeric,
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
const MAX_COMPROMISED_ATTRIBUTES_LENGTH = 200;
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
const maxCompromisedAttributesLength: ConfigurableValidator = maxLength(
  MAX_COMPROMISED_ATTRIBUTES_LENGTH
);

const DescriptionView: React.FC = (): JSX.Element => {
  const { findingId, projectName } = useParams<{
    findingId: string;
    projectName: string;
  }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  // State management
  const dispatch: Dispatch = useDispatch();

  // eslint-disable-next-line @typescript-eslint/ban-types -- redux-form uses "{}" convention
  const isDescriptionPristine: boolean = useSelector((state: {}): boolean =>
    isPristine("editDescription")(state)
  );

  const [isEditing, setEditing] = useState(false);
  const toggleEdit: () => void = useCallback((): void => {
    if (!isDescriptionPristine) {
      dispatch(reset("editDescription"));
    }
    setEditing(!isEditing);
  }, [isDescriptionPristine, dispatch, isEditing]);

  // GraphQL operations
  const { data, refetch } = useQuery<
    IFindingDescriptionData,
    IFindingDescriptionVars
  >(GET_FINDING_DESCRIPTION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading finding description", error);
      });
    },
    variables: {
      canRetrieveAnalyst: permissions.can(
        "backend_api_resolvers_finding_analyst_resolve"
      ),
      canRetrieveSorts: permissions.can(
        "backend_api_resolvers_finding_sorts_resolve"
      ),
      findingId,
      projectName,
    },
  });

  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION, {
    onCompleted: async (result: {
      updateDescription: { success: boolean };
    }): Promise<void> => {
      if (result.updateDescription.success) {
        msgSuccess(
          translate.t("groupAlerts.updated"),
          translate.t("groupAlerts.updatedTitle")
        );
        await refetch();
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid field in form":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - Invalid characters":
            msgError(translate.t("validations.invalidChar"));
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred updating treatment", updateError);
        }
      });
    },
  });

  const handleDescriptionSubmit: (
    values: Dictionary<string>
  ) => Promise<void> = useCallback(
    async (values: Dictionary<string>): Promise<void> => {
      setEditing(false);
      await updateDescription({
        variables: {
          ...values,
          compromisedRecords: Number(values.compromisedRecords),
          findingId,
        },
      });
    },
    [findingId, updateDescription]
  );

  const handleSubmit: () => void = useCallback((): void => {
    if (!isDescriptionPristine) {
      dispatch(submit("editDescription"));
    }
  }, [dispatch, isDescriptionPristine]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset: IFinding = data.finding;

  return (
    <React.StrictMode>
      <ActionButtons
        isEditing={isEditing}
        isPristine={isDescriptionPristine}
        onEdit={toggleEdit}
        onUpdate={handleSubmit}
      />
      <br />
      <GenericForm
        initialValues={dataset}
        name={"editDescription"}
        onSubmit={handleDescriptionSubmit}
      >
        <div>
          <div>
            <Row>
              <Col45>
                <Can
                  do={"backend_api_mutations_update_finding_description_mutate"}
                  passThrough={true}
                >
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={Dropdown}
                      currentValue={formatFindingType(dataset.type)}
                      label={translate.t(
                        "searchFindings.tabDescription.type.title"
                      )}
                      name={"type"}
                      renderAsEditable={isEditing}
                      validate={required}
                      visibleWhileEditing={canEdit}
                    >
                      <option value={""} />
                      <option value={"SECURITY"}>
                        {translate.t(
                          "searchFindings.tabDescription.type.security"
                        )}
                      </option>
                      <option value={"HYGIENE"}>
                        {translate.t(
                          "searchFindings.tabDescription.type.hygiene"
                        )}
                      </option>
                    </EditableField>
                  )}
                </Can>
              </Col45>
              <Can do={"backend_api_resolvers_finding_analyst_resolve"}>
                <Col45>
                  <FormGroup>
                    <ControlLabel>
                      <b>
                        {translate.t("searchFindings.tabDescription.analyst")}
                      </b>
                    </ControlLabel>
                    <p className={"ma0"}>{dataset.analyst}</p>
                  </FormGroup>
                </Col45>
              </Can>
            </Row>
            <Can do={"backend_api_mutations_update_finding_description_mutate"}>
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
                          component={Text}
                          name={"title"}
                          type={"text"}
                          validate={[
                            required,
                            validDraftTitle,
                            validTextField,
                            maxTitleLength,
                          ]}
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
                  do={"backend_api_mutations_update_finding_description_mutate"}
                  passThrough={true}
                >
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
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
                      validate={[
                        required,
                        validTextField,
                        maxDescriptionLength,
                      ]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col100>
            </Row>
            <Row>
              <Col100>
                <Can
                  do={"backend_api_mutations_update_finding_description_mutate"}
                  passThrough={true}
                >
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
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
                      validate={[
                        required,
                        validTextField,
                        maxRequirementsLength,
                      ]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col100>
            </Row>
            <Row>
              <Col45>
                <Can
                  do={"backend_api_mutations_update_finding_description_mutate"}
                  passThrough={true}
                >
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.attackVectorDesc}
                      id={"searchFindings.tabDescription.attackVectors.tooltip"}
                      label={translate.t(
                        "searchFindings.tabDescription.attackVectors.text"
                      )}
                      name={"attackVectorDesc"}
                      renderAsEditable={isEditing}
                      tooltip={translate.t(
                        "searchFindings.tabDescription.attackVectors.tooltip"
                      )}
                      type={"text"}
                      validate={[required, validTextField, maxImpactsLength]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col45>
              <Col45>
                <Can
                  do={"backend_api_mutations_update_finding_description_mutate"}
                  passThrough={true}
                >
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.affectedSystems}
                      id={
                        "searchFindings.tabDescription.affectedSystems.tooltip"
                      }
                      label={translate.t(
                        "searchFindings.tabDescription.affectedSystems.text"
                      )}
                      name={"affectedSystems"}
                      renderAsEditable={isEditing}
                      tooltip={translate.t(
                        "searchFindings.tabDescription.affectedSystems.tooltip"
                      )}
                      type={"text"}
                      validate={[
                        required,
                        validTextField,
                        maxAffectedSystemsLength,
                      ]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col45>
            </Row>
            <Row>
              <Col45>
                <Can
                  do={"backend_api_mutations_update_finding_description_mutate"}
                  passThrough={true}
                >
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
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
                      validate={[required, validTextField, maxThreatLength]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col45>
              <Col45>
                <Can
                  do={"backend_api_mutations_update_finding_description_mutate"}
                  passThrough={true}
                >
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={formatCweUrl(dataset.cweUrl)}
                      id={"searchFindings.tabDescription.weakness.tooltip"}
                      label={translate.t(
                        "searchFindings.tabDescription.weakness.text"
                      )}
                      name={"cweUrl"}
                      renderAsEditable={isEditing}
                      tooltip={translate.t(
                        "searchFindings.tabDescription.weakness.tooltip"
                      )}
                      type={"number"}
                      validate={[required, numeric]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col45>
            </Row>
            <Row>
              <Col100>
                <Can
                  do={"backend_api_mutations_update_finding_description_mutate"}
                  passThrough={true}
                >
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.recommendation}
                      id={
                        "searchFindings.tabDescription.recommendation.tooltip"
                      }
                      label={translate.t(
                        "searchFindings.tabDescription.recommendation.text"
                      )}
                      name={"recommendation"}
                      renderAsEditable={isEditing}
                      tooltip={translate.t(
                        "searchFindings.tabDescription.recommendation.tooltip"
                      )}
                      type={"text"}
                      validate={[
                        required,
                        validTextField,
                        maxRecommendationLength,
                      ]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col100>
            </Row>
            <Row>
              <Col45>
                <Can
                  do={"backend_api_mutations_update_finding_description_mutate"}
                  passThrough={true}
                >
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.compromisedAttributes}
                      id={
                        "searchFindings.tabDescription.compromisedAttrs.tooltip"
                      }
                      label={translate.t(
                        "searchFindings.tabDescription.compromisedAttrs.text"
                      )}
                      name={"compromisedAttributes"}
                      renderAsEditable={isEditing}
                      tooltip={translate.t(
                        "searchFindings.tabDescription.compromisedAttrs.tooltip"
                      )}
                      type={"text"}
                      validate={[
                        validTextField,
                        maxCompromisedAttributesLength,
                      ]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col45>
              <Col45>
                <Can
                  do={"backend_api_mutations_update_finding_description_mutate"}
                  passThrough={true}
                >
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={formatCompromisedRecords(
                        dataset.compromisedRecords
                      )}
                      id={
                        "searchFindings.tabDescription.compromisedRecords.tooltip"
                      }
                      label={translate.t(
                        "searchFindings.tabDescription.compromisedRecords.text"
                      )}
                      name={"compromisedRecords"}
                      renderAsEditable={isEditing}
                      tooltip={translate.t(
                        "searchFindings.tabDescription.compromisedRecords.tooltip"
                      )}
                      type={"number"}
                      validate={[required, numeric]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col45>
            </Row>
            <Can do={"backend_api_mutations_update_finding_description_mutate"}>
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
                          component={Dropdown}
                          name={"sorts"}
                          type={"text"}
                          validate={[required]}
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
      </GenericForm>
    </React.StrictMode>
  );
};

export { DescriptionView };
