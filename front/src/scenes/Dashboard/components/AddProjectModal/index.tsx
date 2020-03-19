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
import { change, EventWithDataHandler, Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal/index";
import store from "../../../../store";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { dropdownField, textField } from "../../../../utils/forms/fields";
import { msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { GenericForm } from "../../components/GenericForm";
import { PROJECTS_QUERY } from "../../containers/HomeView/queries";
import { CREATE_PROJECT_MUTATION, PROJECTS_NAME_QUERY } from "./queries";
import { IAddProjectModal, IProjectName } from "./types";

const addProjectModal: ((props: IAddProjectModal) => JSX.Element) = (props: IAddProjectModal): JSX.Element => {
  const { userOrganization, userRole } = (window as typeof window & { userOrganization: string; userRole: string });
  const [hasForces, setHasForces] = React.useState(true);
  const [canHaveForces, setCanHaveForces] = React.useState(true);
  const [projectName, setProjectName] = React.useState("");
  const isAdmin: boolean  = _.includes(["admin"], userRole);
  const closeNewProjectModal: (() => void) = (): void => { props.onClose(); };
  const handleProjectNameError: ((error: ApolloError) => void) = (error: ApolloError): void => {
    closeNewProjectModal();
    handleGraphQLErrors("An error occurred getting project name", error);
  };
  const handleProjectNameResult: ((qrResult: IProjectName) => void) = (qrResult: IProjectName): void => {
    if (!_.isUndefined(qrResult)) {
      store.dispatch(change("newProject", "name", qrResult.internalProjectNames.projectName.toUpperCase()));
      setProjectName(qrResult.internalProjectNames.projectName);
    }
  };

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
          onCompleted={handleProjectNameResult}
          onError={handleProjectNameError}
        >
          {({}: QueryResult<IProjectName>): JSX.Element => {
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
            const handleForcesButtonChange: (() => void) = (): void => { setHasForces(!hasForces); };
            const handleSubscriptionTypeChange: EventWithDataHandler<React.ChangeEvent<string>> =
            (event: React.ChangeEvent<string> | undefined, subscriptionType: string): void => {
              setCanHaveForces(subscriptionType === "Continuous");
              setHasForces(subscriptionType === "Continuous");
            };

            return (
              <Mutation
                mutation={CREATE_PROJECT_MUTATION}
                onCompleted={handleMutationResult}
                onError={handleCreateError}
                refetchQueries={[{ query: PROJECTS_QUERY}]}
              >
                {(createProject: MutationFunction, { loading: submitting }: MutationResult): JSX.Element => {
                  if (!isAdmin) { store.dispatch(change("newProject", "company", userOrganization)); }

                  const handleSubmit: ((values: { company: string; description: string; type: string }) => void) =
                  (values: { company: string; description: string; type: string }): void => {
                    const companies: string[] = isAdmin ? values.company.split(",") : [userOrganization];

                    createProject({ variables: {
                      companies,
                      description: values.description,
                      hasForces,
                      projectName,
                      subscription: values.type,
                    }})
                    .catch();
                  };

                  return (
                    <GenericForm name="newProject" onSubmit={handleSubmit}>
                      {({ pristine }: InjectedFormProps): JSX.Element => (
                        <React.Fragment>
                          <Row>
                            <Col md={12} sm={12}>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newProject.company")}</ControlLabel>
                                <Field
                                  component={textField}
                                  disabled={!isAdmin}
                                  name="company"
                                  type="text"
                                  validate={[required]}
                                />
                              </FormGroup>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newProject.name")}</ControlLabel>
                                <Field
                                  component={textField}
                                  disabled={true}
                                  name="name"
                                  type="text"
                                  validate={[required]}
                                />
                              </FormGroup>
                              <FormGroup>
                                <ControlLabel>{translate.t("home.newProject.description")}</ControlLabel>
                                <Field
                                  component={textField}
                                  name="description"
                                  type="text"
                                  validate={[required]}
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
                          {canHaveForces
                            ? <Row>
                                <Col md={5} sm={5}>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("home.newProject.forces.title")}</ControlLabel>
                                    <BootstrapSwitchButton
                                      checked={hasForces}
                                      offlabel={translate.t("home.newProject.forces.no")}
                                      onChange={handleForcesButtonChange}
                                      onlabel={translate.t("home.newProject.forces.yes")}
                                      onstyle="danger"
                                      style="btn-block"
                                    />
                                  </FormGroup>
                                </Col>
                              </Row>
                            : <div />}
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
