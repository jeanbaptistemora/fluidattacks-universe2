/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import BootstrapSwitchButton from "bootstrap-switch-button-react";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { EventWithDataHandler, Field, InjectedFormProps } from "redux-form";
import { ConfigurableValidator } from "revalidate";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal/index";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { dropdownField, textField } from "../../../../utils/forms/fields";
import { msgSuccess } from "../../../../utils/notifications";
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

  const [canHaveDrills, setCanHaveDrills] = React.useState(true);
  const [canHaveForces, setCanHaveForces] = React.useState(true);

  const [subscriptionType, setSubscriptionType] = React.useState("CONTINUOUS");

  const closeNewProjectModal: (() => void) = (): void => { props.onClose(); };
  const handleProjectNameError: ((error: ApolloError) => void) = (error: ApolloError): void => {
    closeNewProjectModal();
    handleGraphQLErrors("An error occurred getting project name", error);
  };

  const isContinuousType: ((subsType: string) => boolean) =
    (subsType: string): boolean => subsType === "CONTINUOUS";

  return (
    <React.StrictMode>
      <Modal
        footer={<div />}
        headerTitle={translate.t("home.newProject.new")}
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
                  translate.t("home.newProject.success"),
                  translate.t("home.newProject.titleSuccess"),
                );
              }
            };
            const handleCreateError: ((error: ApolloError) => void) = (error: ApolloError): void => {
              handleGraphQLErrors("An error occurred adding a project", error);
            };

            const handleSubscriptionTypeChange: EventWithDataHandler<React.ChangeEvent<string>> = (
              event: React.ChangeEvent<string> | undefined, subsType: string,
            ): void => {
              setSubscriptionType(subsType);

              setHasDrills(isContinuousType(subsType));
              setHasForces(isContinuousType(subsType));

              setCanHaveDrills(isContinuousType(subsType));
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

            return (
              <Mutation
                mutation={CREATE_PROJECT_MUTATION}
                onCompleted={handleMutationResult}
                onError={handleCreateError}
                refetchQueries={[{ query: PROJECTS_QUERY }]}
              >
                {(createProject: MutationFunction, { loading: submitting }: MutationResult): JSX.Element => {

                  const handleSubmit: (
                    (values: { company: string; description: string; name: string; type: string }) => void) = (
                    values: { company: string; description: string; name: string; type: string },
                  ): void => {
                    const companies: string[] = values.company.split(",");

                    createProject({
                      variables: {
                        companies,
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
                      name="newProject"
                      initialValues={{ name: projectName.toUpperCase() }}
                      onSubmit={handleSubmit}
                    >
                      {({ pristine }: InjectedFormProps): JSX.Element => (
                        <React.Fragment>
                          <Row>
                            <Col md={12} sm={12}>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newProject.company")}</ControlLabel>
                                <Field
                                  component={textField}
                                  name="company"
                                  type="text"
                                  validate={[required, maxCompanyLength, validTextField]}
                                />
                              </FormGroup>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newProject.name")}</ControlLabel>
                                <Field
                                  component={textField}
                                  name="name"
                                  type="text"
                                  validate={[alphaNumeric, maxProjectNameLength, required, validTextField]}
                                />
                              </FormGroup>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newProject.description")}</ControlLabel>
                                <Field
                                  component={textField}
                                  name="description"
                                  type="text"
                                  validate={[required, maxDescriptionLength, validTextField]}
                                />
                              </FormGroup>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newProject.type.title")}</ControlLabel>
                                <Field
                                  component={dropdownField}
                                  name="type"
                                  onChange={handleSubscriptionTypeChange}
                                >
                                  <option value="CONTINUOUS">{translate.t("home.newProject.type.continuous")}</option>
                                  <option value="ONESHOT">{translate.t("home.newProject.type.one_shot")}</option>
                                </Field>
                              </FormGroup>
                            </Col>
                          </Row>
                          <Row>
                            <Col md={5} sm={5}>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newProject.integrates")}</ControlLabel>
                                <BootstrapSwitchButton
                                  checked={true}
                                  disabled={true}
                                  offlabel={translate.t("home.newProject.switch.no")}
                                  onlabel={translate.t("home.newProject.switch.yes")}
                                  onstyle="danger"
                                  style="btn-block"
                                />
                              </FormGroup>
                            </Col>
                          </Row>
                          {canHaveDrills ? (
                            <Row>
                              <Col md={5} sm={5}>
                                <FormGroup>
                                  <ControlLabel>{translate.t("home.newProject.drills")}</ControlLabel>
                                  <BootstrapSwitchButton
                                    checked={hasDrills}
                                    offlabel={translate.t("home.newProject.switch.no")}
                                    onChange={handleDrillsBtnChange}
                                    onlabel={translate.t("home.newProject.switch.yes")}
                                    onstyle="danger"
                                    style="btn-block"
                                  />
                                </FormGroup>
                              </Col>
                            </Row>
                          ) : undefined}
                          {canHaveForces ? (
                            <Row>
                              <Col md={5} sm={5}>
                                <FormGroup>
                                  <ControlLabel>{translate.t("home.newProject.forces")}</ControlLabel>
                                  <BootstrapSwitchButton
                                    checked={hasForces}
                                    offlabel={translate.t("home.newProject.switch.no")}
                                    onChange={handleForcesBtnChange}
                                    onlabel={translate.t("home.newProject.switch.yes")}
                                    onstyle="danger"
                                    style="btn-block"
                                  />
                                </FormGroup>
                              </Col>
                            </Row>
                          ) : undefined}
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
