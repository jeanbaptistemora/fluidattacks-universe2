/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import { ApolloError } from "apollo-client";
import BootstrapSwitchButton from "bootstrap-switch-button-react";
import { Button } from "components/Button";
import { ConfigurableValidator } from "revalidate";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal/index";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import { translate } from "utils/translations/translate";
import {
  ButtonToolbar,
  Col,
  ControlLabel,
  FormGroup,
  Row,
} from "react-bootstrap";
import {
  CREATE_PROJECT_MUTATION,
  PROJECTS_NAME_QUERY,
} from "scenes/Dashboard/components/AddProjectModal/queries";
import { Dropdown, Text } from "utils/forms/fields";
import { Field, InjectedFormProps } from "redux-form";
import {
  IAddProjectModalProps,
  IProjectNameProps,
} from "scenes/Dashboard/components/AddProjectModal/types";
import { Mutation, Query } from "@apollo/react-components";
import {
  MutationFunction,
  MutationResult,
  QueryResult,
} from "@apollo/react-common";
import {
  alphaNumeric,
  maxLength,
  required,
  validTextField,
} from "utils/validations";
import { msgError, msgSuccess } from "utils/notifications";

/*
 * Business rules to create a project:
 *   - Integrates must enabled, because we are using Integrates right now, right?
 *   - Drills <--needs-- Integrates
 *   - Forces <--needs-- Drills
 *
 * Business rules after creating the project:
 *   - If Integrates is turned off the project will be scheduled for deletion
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
  const { onClose, isOpen, organization } = props;
  // State management
  const [hasDrills, setHasDrills] = React.useState(true);
  const [hasForces, setHasForces] = React.useState(true);

  const [canHaveForces, setCanHaveForces] = React.useState(true);

  const [subscriptionType, setSubscriptionType] = React.useState("CONTINUOUS");

  function closeNewProjectModal(): void {
    onClose();
  }
  function handleProjectNameError({ graphQLErrors }: ApolloError): void {
    closeNewProjectModal();
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - There are no group names available at the moment":
          msgError(
            translate.t("organization.tabs.groups.newGroup.noGroupName")
          );
          break;
        default:
          msgError(translate.t("group_alerts.error_textsad"));
          Logger.warning("An error occurred adding access token", error);
      }
    });
  }

  const isContinuousType: (subsType: string) => boolean = (
    subsType: string
  ): boolean => subsType === "CONTINUOUS";

  return (
    <React.StrictMode>
      <Modal
        footer={<div />}
        headerTitle={translate.t("organization.tabs.groups.newGroup.new.group")}
        onClose={closeNewProjectModal}
        open={isOpen}
      >
        <Query
          fetchPolicy={"network-only"}
          onError={handleProjectNameError}
          query={PROJECTS_NAME_QUERY}
        >
          {({ data }: QueryResult<IProjectNameProps>): JSX.Element => {
            const projectName: string =
              _.isUndefined(data) || _.isEmpty(data)
                ? ""
                : data.internalNames.name;

            function handleMutationResult(result: {
              createProject: { success: boolean };
            }): void {
              if (result.createProject.success) {
                closeNewProjectModal();
                msgSuccess(
                  translate.t("organization.tabs.groups.newGroup.success"),
                  translate.t("organization.tabs.groups.newGroup.titleSuccess")
                );
              }
            }

            function handleCreateError({ graphQLErrors }: ApolloError): void {
              graphQLErrors.forEach((error: GraphQLError): void => {
                switch (error.message) {
                  case "Exception - There are no group names available at the moment":
                    msgError(
                      translate.t(
                        "organization.tabs.groups.newGroup.noGroupName"
                      )
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
                    msgError(translate.t("group_alerts.error_textsad"));
                    Logger.warning("An error occurred adding a project", error);
                }
              });
            }

            function handleSubscriptionTypeChange(
              _event: React.ChangeEvent<string> | undefined,
              subsType: string
            ): void {
              setSubscriptionType(subsType);

              setHasDrills(true);
              setHasForces(isContinuousType(subsType));

              setCanHaveForces(isContinuousType(subsType));
            }
            function handleDrillsBtnChange(withDrills: boolean): void {
              setHasDrills(withDrills);

              if (!withDrills) {
                setHasForces(false);
              }

              setCanHaveForces(
                withDrills && isContinuousType(subscriptionType)
              );
            }
            function handleForcesBtnChange(withForces: boolean): void {
              setHasForces(withForces);
            }

            return (
              <Mutation
                mutation={CREATE_PROJECT_MUTATION}
                onCompleted={handleMutationResult}
                onError={handleCreateError}
              >
                {(
                  createProject: MutationFunction,
                  { loading: submitting }: MutationResult
                ): JSX.Element => {
                  function handleSubmit(values: {
                    description: string;
                    name: string;
                    organization: string;
                    type: string;
                  }): void {
                    void createProject({
                      variables: {
                        description: values.description,
                        hasDrills,
                        hasForces,
                        organization: values.organization,
                        projectName: values.name,
                        subscription: values.type,
                      },
                    });
                  }

                  return (
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
                            <Col md={12} sm={12}>
                              <FormGroup>
                                <ControlLabel>
                                  {translate.t(
                                    "organization.tabs.groups.newGroup.organization.text"
                                  )}
                                </ControlLabel>
                                <TooltipWrapper
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
                                  {translate.t(
                                    "organization.tabs.groups.newGroup.name"
                                  )}
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
                                  message={translate.t(
                                    "organization.tabs.groups.newGroup.description.tooltip"
                                  )}
                                  placement={"top"}
                                >
                                  <FormGroup>
                                    <Field
                                      component={Text}
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
                                          "organization.tabs.groups.newGroup.type.one_shot"
                                        )}
                                      </option>
                                    </Field>
                                  </FormGroup>
                                </TooltipWrapper>
                              </FormGroup>
                            </Col>
                          </Row>
                          <Row>
                            <Col md={5} sm={5}>
                              <TooltipWrapper
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
                                  <BootstrapSwitchButton
                                    checked={true}
                                    disabled={true}
                                    offlabel={translate.t(
                                      "organization.tabs.groups.newGroup.switch.no"
                                    )}
                                    onlabel={translate.t(
                                      "organization.tabs.groups.newGroup.switch.yes"
                                    )}
                                    onstyle={"danger"}
                                    //Allow style on bootstrap component
                                    //eslint-disable-next-line react/style-prop-object
                                    style={"btn-block"}
                                  />
                                </FormGroup>
                              </TooltipWrapper>
                            </Col>
                          </Row>
                          <Row>
                            <Col md={5} sm={5}>
                              <TooltipWrapper
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
                                  <BootstrapSwitchButton
                                    checked={hasDrills}
                                    offlabel={translate.t(
                                      "organization.tabs.groups.newGroup.switch.no"
                                    )}
                                    onChange={handleDrillsBtnChange}
                                    onlabel={translate.t(
                                      "organization.tabs.groups.newGroup.switch.yes"
                                    )}
                                    onstyle={"danger"}
                                    //Allow style on bootstrap component
                                    //eslint-disable-next-line react/style-prop-object
                                    style={"btn-block"}
                                  />
                                </FormGroup>
                              </TooltipWrapper>
                            </Col>
                          </Row>
                          {canHaveForces ? (
                            <Row>
                              <Col md={5} sm={5}>
                                <TooltipWrapper
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
                                    <BootstrapSwitchButton
                                      checked={hasForces}
                                      offlabel={translate.t(
                                        "organization.tabs.groups.newGroup.switch.no"
                                      )}
                                      onChange={handleForcesBtnChange}
                                      onlabel={translate.t(
                                        "organization.tabs.groups.newGroup.switch.yes"
                                      )}
                                      onstyle={"danger"}
                                      //Allow style on bootstrap component
                                      //eslint-disable-next-line react/style-prop-object
                                      style={"btn-block"}
                                    />
                                  </FormGroup>
                                </TooltipWrapper>
                              </Col>
                            </Row>
                          ) : undefined}
                          {" *"}
                          {translate.t(
                            "organization.tabs.groups.newGroup.extra_charges_may_apply"
                          )}
                          <br />
                          <ButtonToolbar className={"pull-right"}>
                            <Button
                              bsStyle={"success"}
                              onClick={closeNewProjectModal}
                            >
                              {translate.t("confirmmodal.cancel")}
                            </Button>
                            <Button
                              bsStyle={"success"}
                              disabled={pristine || submitting}
                              type={"submit"}
                            >
                              {translate.t("confirmmodal.proceed")}
                            </Button>
                          </ButtonToolbar>
                        </React.Fragment>
                      )}
                    </GenericForm>
                  );
                }}
              </Mutation>
            );
          }}
        </Query>
      </Modal>
    </React.StrictMode>
  );
};

export { AddProjectModal };
