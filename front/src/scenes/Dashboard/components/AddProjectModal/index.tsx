/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import BootstrapSwitchButton from "bootstrap-switch-button-react";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { EventWithDataHandler, Field, InjectedFormProps } from "redux-form";
import { ConfigurableValidator } from "revalidate";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal/index";
import { TooltipWrapper } from "../../../../components/TooltipWrapper";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import { dropdownField, textField } from "../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { alphaNumeric, maxLength, required, validTextField } from "../../../../utils/validations";
import { GenericForm } from "../../components/GenericForm";
import { PROJECTS_QUERY } from "../../containers/HomeView/queries";
import { CREATE_PROJECT_MUTATION, PROJECTS_NAME_QUERY } from "./queries";
import { IAddProjectModal, IProjectName } from "./types";

/*
  * Business rules to create a project:
  *   - Integrates must enabled, because we are using Integrates right now, right?
  *   - Drills <--needs-- Integrates
  *   - Forces <--needs-- Drills
  *
  * Business rules after creating the project:
  *   - If Integrates is turned off the project will be scheduled for deletion
  */

const maxDescriptionLength: ConfigurableValidator = maxLength(200);
const maxProjectNameLength: ConfigurableValidator = maxLength(20);
const maxCompanyLength: ConfigurableValidator = maxLength(50);
const addProjectModal: ((props: IAddProjectModal) => JSX.Element) = (props: IAddProjectModal): JSX.Element => {
  // State management
  const [hasDrills, setHasDrills] = React.useState(true);
  const [hasForces, setHasForces] = React.useState(true);

  const [canHaveForces, setCanHaveForces] = React.useState(true);

  const [subscriptionType, setSubscriptionType] = React.useState("CONTINUOUS");

  const closeNewProjectModal: (() => void) = (): void => { props.onClose(); };
  const handleProjectNameError: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    closeNewProjectModal();
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - There are no group names available at the moment":
          msgError(translate.t("home.newGroup.noGroupName"));
          break;
        default:
          msgError(translate.t("group_alerts.error_textsad"));
          rollbar.error("An error occurred adding access token", error);
      }
    });
  };

  const isContinuousType: ((subsType: string) => boolean) =
    (subsType: string): boolean => subsType === "CONTINUOUS";

  return (
    <React.StrictMode>
      <Modal
        footer={<div />}
        headerTitle={translate.t("home.newGroup.new.group")}
        onClose={closeNewProjectModal}
        open={props.isOpen}
      >
        <Query
          query={PROJECTS_NAME_QUERY}
          fetchPolicy="network-only"
          onError={handleProjectNameError}
        >
          {({ data }: QueryResult<IProjectName>): JSX.Element => {
            const projectName: string = _.isUndefined(data) || _.isEmpty(data)
              ? ""
              : data.internalProjectNames.projectName;

            const handleMutationResult: ((result: { createProject: { success: boolean } }) => void) = (
              result: { createProject: { success: boolean } },
            ): void => {
              if (result.createProject.success) {
                closeNewProjectModal();
                msgSuccess(
                  translate.t("home.newGroup.success"),
                  translate.t("home.newGroup.titleSuccess"),
                );
              }
            };
            const handleCreateError: ((error: ApolloError) => void) = (
              { graphQLErrors }: ApolloError,
            ): void => {
              graphQLErrors.forEach((error: GraphQLError): void => {
                switch (error.message) {
                  case "Exception - There are no group names available at the moment":
                    msgError(translate.t("home.newGroup.noGroupName"));
                    break;
                  case "Exception - Error invalid project name":
                    msgError(translate.t("home.newGroup.invalidGroup"));
                    break;
                  case "Exception - Organization name is invalid":
                    msgError(translate.t("home.newGroup.invalidOrganizationName"));
                    break;
                  case "Exception - User is not a member of the target organization":
                    msgError(translate.t("home.newGroup.userNotInOrganization"));
                    break;
                  default:
                    msgError(translate.t("group_alerts.error_textsad"));
                    rollbar.error("An error occurred adding a project", error);
                }
              });
            };

            const handleSubscriptionTypeChange: EventWithDataHandler<React.ChangeEvent<string>> = (
              event: React.ChangeEvent<string> | undefined, subsType: string,
            ): void => {
              setSubscriptionType(subsType);

              setHasDrills(true);
              setHasForces(isContinuousType(subsType));

              setCanHaveForces(isContinuousType(subsType));
            };
            const handleDrillsBtnChange: ((withDrills: boolean) => void) = (withDrills: boolean): void => {
              setHasDrills(withDrills);

              if (!withDrills) {
                setHasForces(false);
              }

              setCanHaveForces(withDrills && isContinuousType(subscriptionType));
            };
            const handleForcesBtnChange: ((withForces: boolean) => void) = (withForces: boolean): void => {
              setHasForces(withForces);
            };

            const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
            const variables: { tagsField: boolean } = {
              tagsField: permissions.can("backend_api_resolvers_me__get_tags"),
            };

            return (
              <Mutation
                mutation={CREATE_PROJECT_MUTATION}
                onCompleted={handleMutationResult}
                onError={handleCreateError}
                refetchQueries={[{ query: PROJECTS_QUERY, variables }]}
              >
                {(createProject: MutationFunction, { loading: submitting }: MutationResult): JSX.Element => {

                  const handleSubmit: (
                    (values: { company: string; description: string; name: string; type: string }) => void) = (
                    values: { company: string; description: string; name: string; type: string },
                  ): void => {

                    createProject({
                      variables: {
                        company: values.company,
                        description: values.description,
                        hasDrills,
                        hasForces,
                        projectName: values.name,
                        subscription: values.type,
                      },
                    })
                      .catch();
                  };

                  return (
                    <GenericForm
                      name="newGroup"
                      initialValues={{ name: projectName.toUpperCase() }}
                      onSubmit={handleSubmit}
                    >
                      {({ pristine }: InjectedFormProps): JSX.Element => (
                        <React.Fragment>
                          <Row>
                            <Col md={12} sm={12}>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newGroup.company.text")}</ControlLabel>
                                <TooltipWrapper
                                  message={translate.t("home.newGroup.company.tooltip")}
                                  placement="top"
                                >
                                  <FormGroup>
                                    <Field
                                      component={textField}
                                      name="company"
                                      type="text"
                                      validate={[required, maxCompanyLength, validTextField]}
                                    />
                                  </FormGroup>
                                </TooltipWrapper>
                              </FormGroup>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newGroup.name")}</ControlLabel>
                                <Field
                                  component={textField}
                                  disabled={true}
                                  name="name"
                                  type="text"
                                  validate={[alphaNumeric, maxProjectNameLength, required, validTextField]}
                                />
                              </FormGroup>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newGroup.description.text")}</ControlLabel>
                                <TooltipWrapper
                                  message={translate.t("home.newGroup.description.tooltip")}
                                  placement="top"
                                >
                                  <FormGroup>
                                    <Field
                                      component={textField}
                                      name="description"
                                      type="text"
                                      validate={[required, maxDescriptionLength, validTextField]}
                                    />
                                  </FormGroup>
                                </TooltipWrapper>
                              </FormGroup>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newGroup.type.title")}</ControlLabel>
                                <TooltipWrapper
                                  message={translate.t("home.newGroup.type.tooltip")}
                                  placement="top"
                                >
                                  <FormGroup>
                                    <Field
                                      component={dropdownField}
                                      name="type"
                                      onChange={handleSubscriptionTypeChange}
                                    >
                                      <option value="CONTINUOUS">{translate.t("home.newGroup.type.continuous")}</option>
                                      <option value="ONESHOT">{translate.t("home.newGroup.type.one_shot")}</option>
                                    </Field>
                                  </FormGroup>
                                </TooltipWrapper>
                              </FormGroup>
                            </Col>
                          </Row>
                          <Row>
                            <Col md={5} sm={5}>
                              <TooltipWrapper message={translate.t("home.newGroup.integrates.tooltip")} placement="top">
                                <FormGroup>
                                  <ControlLabel>{translate.t("home.newGroup.integrates.text")} *</ControlLabel>
                                  <BootstrapSwitchButton
                                    checked={true}
                                    disabled={true}
                                    offlabel={translate.t("home.newGroup.switch.no")}
                                    onlabel={translate.t("home.newGroup.switch.yes")}
                                    onstyle="danger"
                                    style="btn-block"
                                  />
                                </FormGroup>
                              </TooltipWrapper>
                            </Col>
                          </Row>
                          <Row>
                            <Col md={5} sm={5}>
                              <TooltipWrapper message={translate.t("home.newGroup.drills.tooltip")} placement="top">
                                <FormGroup>
                                  <ControlLabel>{translate.t("home.newGroup.drills.text")} *</ControlLabel>
                                  <BootstrapSwitchButton
                                    checked={hasDrills}
                                    offlabel={translate.t("home.newGroup.switch.no")}
                                    onChange={handleDrillsBtnChange}
                                    onlabel={translate.t("home.newGroup.switch.yes")}
                                    onstyle="danger"
                                    style="btn-block"
                                  />
                                </FormGroup>
                              </TooltipWrapper>
                            </Col>
                          </Row>
                          {canHaveForces ? (
                            <Row>
                              <Col md={5} sm={5}>
                                <TooltipWrapper
                                  message={translate.t("home.newGroup.forces.tooltip")}
                                  placement="top"
                                >
                                  <FormGroup>
                                    <ControlLabel>{translate.t("home.newGroup.forces.text")} *</ControlLabel>
                                    <BootstrapSwitchButton
                                      checked={hasForces}
                                      offlabel={translate.t("home.newGroup.switch.no")}
                                      onChange={handleForcesBtnChange}
                                      onlabel={translate.t("home.newGroup.switch.yes")}
                                      onstyle="danger"
                                      style="btn-block"
                                    />
                                  </FormGroup>
                                </TooltipWrapper>
                              </Col>
                            </Row>
                          ) : undefined}
                          * {translate.t("home.newGroup.extra_charges_may_apply")}
                          <br />
                          <ButtonToolbar className="pull-right">
                            <Button bsStyle="success" onClick={closeNewProjectModal}>
                              {translate.t("confirmmodal.cancel")}
                            </Button>
                            <Button bsStyle="success" type="submit" disabled={pristine || submitting}>
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

export { addProjectModal as AddProjectModal };
