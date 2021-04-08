import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { Field } from "redux-form";
import type { InjectedFormProps } from "redux-form";
import type { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { SwitchButton } from "components/SwitchButton";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  CREATE_PROJECT_MUTATION,
  PROJECTS_NAME_QUERY,
} from "scenes/Dashboard/components/AddProjectModal/queries";
import type { IAddProjectModalProps } from "scenes/Dashboard/components/AddProjectModal/types";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  ButtonToolbar,
  Col100,
  Col40,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Dropdown, Text } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  alphaNumeric,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

/*
 * Business rules to create a project:
 *   - Integrates must enabled, because we are using Integrates right now, right?
 *   - Drills <--needs-- Integrates
 *   - Forces <--needs-- Drills
 *
 * Business rules after creating the project:
 *   - If Integrates is turned off the project will be immediately deleted
 */

const MAX_DESCRIPTION_LENGTH: number = 200;
const MAX_PROJECT_NAME_LENGTH: number = 20;
const MAX_ORGANIZATION_LENGTH: number = 50;

const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);
const maxProjectNameLength: ConfigurableValidator = maxLength(
  MAX_PROJECT_NAME_LENGTH
);
const maxOrganizationLength: ConfigurableValidator = maxLength(
  MAX_ORGANIZATION_LENGTH
);
const AddProjectModal: React.FC<IAddProjectModalProps> = (
  props: IAddProjectModalProps
): JSX.Element => {
  const { onClose, organization } = props;
  // State management
  const [hasDrills, setHasDrills] = useState(true);
  const [hasForces, setHasForces] = useState(true);

  const [canHaveForces, setCanHaveForces] = useState(true);

  const [subscriptionType, setSubscriptionType] = useState("CONTINUOUS");

  const isContinuousType: (subsType: string) => boolean = (
    subsType: string
  ): boolean => subsType === "CONTINUOUS";

  const handleMutationResult = (result: {
    createProject: { success: boolean };
  }): void => {
    if (result.createProject.success) {
      onClose();
      msgSuccess(
        translate.t("organization.tabs.groups.newGroup.success"),
        translate.t("organization.tabs.groups.newGroup.titleSuccess")
      );
    }
  };

  const handleCreateError = ({ graphQLErrors }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - There are no group names available at the moment":
          msgError(
            translate.t("organization.tabs.groups.newGroup.noGroupName")
          );
          break;
        case "Exception - User is not a member of the target organization":
          msgError(
            translate.t(
              "organization.tabs.groups.newGroup.userNotInOrganization"
            )
          );
          break;
        default:
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred adding a project", error);
      }
    });
  };

  const handleSubscriptionTypeChange = useCallback(
    (_event: React.ChangeEvent<string> | undefined, subsType: string): void => {
      setSubscriptionType(subsType);

      setHasDrills(true);
      setHasForces(isContinuousType(subsType));

      setCanHaveForces(isContinuousType(subsType));
    },
    []
  );

  const handleDrillsBtnChange = useCallback(
    (withDrills: boolean): void => {
      setHasDrills(withDrills);

      if (!withDrills) {
        setHasForces(false);
      }

      setCanHaveForces(withDrills && isContinuousType(subscriptionType));
    },
    [subscriptionType]
  );

  const handleForcesBtnChange = useCallback((withForces: boolean): void => {
    setHasForces(withForces);
  }, []);

  const [createProject, { loading: submitting }] = useMutation(
    CREATE_PROJECT_MUTATION,
    {
      onCompleted: handleMutationResult,
      onError: handleCreateError,
    }
  );

  const handleSubmit = useCallback(
    (values: {
      description: string;
      name: string;
      language: string;
      organization: string;
      type: string;
    }): void => {
      track("AddGroup");
      void createProject({
        variables: {
          description: values.description,
          hasDrills,
          hasForces,
          language: values.language,
          organization: values.organization,
          projectName: values.name,
          subscription: values.type,
        },
      });
    },
    [createProject, hasDrills, hasForces]
  );

  function handleProjectNameError({ graphQLErrors }: ApolloError): void {
    onClose();
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - There are no group names available at the moment":
          msgError(
            translate.t("organization.tabs.groups.newGroup.noGroupName")
          );
          break;
        default:
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred adding access token", error);
      }
    });
  }

  const { data } = useQuery(PROJECTS_NAME_QUERY, {
    fetchPolicy: "network-only",
    onError: handleProjectNameError,
  });

  const projectName: string =
    // The type was already defined in the schema
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
    _.isUndefined(data) || _.isEmpty(data) ? "" : data.internalNames.name;

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("organization.tabs.groups.newGroup.new.group")}
        open={true}
      >
        <GenericForm
          initialValues={{
            name: projectName.toUpperCase(),
            organization: organization.toUpperCase(),
          }}
          name={"newGroup"}
          onSubmit={handleSubmit}
        >
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <Row>
                <Col100>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t(
                        "organization.tabs.groups.newGroup.organization.text"
                      )}
                    </ControlLabel>
                    <TooltipWrapper
                      id={
                        "organization.tabs.groups.newGroup.organization.tooltip"
                      }
                      message={translate.t(
                        "organization.tabs.groups.newGroup.organization.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <Field
                          component={Text}
                          disabled={true}
                          name={"organization"}
                          type={"text"}
                          validate={[
                            required,
                            maxOrganizationLength,
                            validTextField,
                          ]}
                        />
                      </FormGroup>
                    </TooltipWrapper>
                  </FormGroup>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("organization.tabs.groups.newGroup.name")}
                    </ControlLabel>
                    <Field
                      component={Text}
                      disabled={true}
                      name={"name"}
                      type={"text"}
                      validate={[
                        alphaNumeric,
                        maxProjectNameLength,
                        required,
                        validTextField,
                      ]}
                    />
                  </FormGroup>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t(
                        "organization.tabs.groups.newGroup.description.text"
                      )}
                    </ControlLabel>
                    <TooltipWrapper
                      id={
                        "organization.tabs.groups.newGroup.description.tooltip"
                      }
                      message={translate.t(
                        "organization.tabs.groups.newGroup.description.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <Field
                          component={Text}
                          id={"add-group-description"}
                          name={"description"}
                          type={"text"}
                          validate={[
                            required,
                            maxDescriptionLength,
                            validTextField,
                          ]}
                        />
                      </FormGroup>
                    </TooltipWrapper>
                  </FormGroup>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t(
                        "organization.tabs.groups.newGroup.type.title"
                      )}
                    </ControlLabel>
                    <TooltipWrapper
                      id={"organization.tabs.groups.newGroup.type.tooltip"}
                      message={translate.t(
                        "organization.tabs.groups.newGroup.type.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <Field
                          component={Dropdown}
                          name={"type"}
                          onChange={handleSubscriptionTypeChange}
                        >
                          <option value={"CONTINUOUS"}>
                            {translate.t(
                              "organization.tabs.groups.newGroup.type.continuous"
                            )}
                          </option>
                          <option value={"ONESHOT"}>
                            {translate.t(
                              "organization.tabs.groups.newGroup.type.oneShot"
                            )}
                          </option>
                        </Field>
                      </FormGroup>
                    </TooltipWrapper>
                  </FormGroup>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t(
                        "organization.tabs.groups.newGroup.language.text"
                      )}
                    </ControlLabel>
                    <TooltipWrapper
                      id={"organization.tabs.groups.newGroup.language.tooltip"}
                      message={translate.t(
                        "organization.tabs.groups.newGroup.language.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <Field component={Dropdown} name={"language"}>
                          <option value={"EN"}>
                            {translate.t(
                              "organization.tabs.groups.newGroup.language.EN"
                            )}
                          </option>
                          <option value={"ES"}>
                            {translate.t(
                              "organization.tabs.groups.newGroup.language.ES"
                            )}
                          </option>
                        </Field>
                      </FormGroup>
                    </TooltipWrapper>
                  </FormGroup>
                </Col100>
              </Row>
              <Row>
                <Col40>
                  <TooltipWrapper
                    id={"organization.tabs.groups.newGroup.integrates.tooltip"}
                    message={translate.t(
                      "organization.tabs.groups.newGroup.integrates.tooltip"
                    )}
                    placement={"top"}
                  >
                    <FormGroup>
                      <ControlLabel>
                        {translate.t(
                          "organization.tabs.groups.newGroup.integrates.text"
                        )}
                        {" *"}
                      </ControlLabel>
                      <SwitchButton
                        checked={true}
                        disabled={true}
                        offlabel={translate.t(
                          "organization.tabs.groups.newGroup.switch.no"
                        )}
                        onlabel={translate.t(
                          "organization.tabs.groups.newGroup.switch.yes"
                        )}
                      />
                    </FormGroup>
                  </TooltipWrapper>
                </Col40>
              </Row>
              <Row>
                <Col40>
                  <TooltipWrapper
                    id={"organization.tabs.groups.newGroup.drills.tooltip"}
                    message={translate.t(
                      "organization.tabs.groups.newGroup.drills.tooltip"
                    )}
                    placement={"top"}
                  >
                    <FormGroup>
                      <ControlLabel>
                        {translate.t(
                          "organization.tabs.groups.newGroup.drills.text"
                        )}
                        {" *"}
                      </ControlLabel>
                      <SwitchButton
                        checked={hasDrills}
                        offlabel={translate.t(
                          "organization.tabs.groups.newGroup.switch.no"
                        )}
                        onChange={handleDrillsBtnChange}
                        onlabel={translate.t(
                          "organization.tabs.groups.newGroup.switch.yes"
                        )}
                      />
                    </FormGroup>
                  </TooltipWrapper>
                </Col40>
              </Row>
              {canHaveForces ? (
                <Row>
                  <Col40>
                    <TooltipWrapper
                      id={"organization.tabs.groups.newGroup.forces.tooltip"}
                      message={translate.t(
                        "organization.tabs.groups.newGroup.forces.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <ControlLabel>
                          {translate.t(
                            "organization.tabs.groups.newGroup.forces.text"
                          )}
                          {" *"}
                        </ControlLabel>
                        <SwitchButton
                          checked={hasForces}
                          offlabel={translate.t(
                            "organization.tabs.groups.newGroup.switch.no"
                          )}
                          onChange={handleForcesBtnChange}
                          onlabel={translate.t(
                            "organization.tabs.groups.newGroup.switch.yes"
                          )}
                        />
                      </FormGroup>
                    </TooltipWrapper>
                  </Col40>
                </Row>
              ) : undefined}
              {" *"}
              {translate.t(
                "organization.tabs.groups.newGroup.extraChargesMayApply"
              )}
              <hr />
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button id={"add-group-cancel"} onClick={onClose}>
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={pristine || submitting}
                      id={"add-group-proceed"}
                      type={"submit"}
                    >
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </React.Fragment>
          )}
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { AddProjectModal };
