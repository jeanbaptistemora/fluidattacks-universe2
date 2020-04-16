/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for accessing render props from apollo components
 */
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";
import { Modal } from "../../../../components/Modal";
import { Can } from "../../../../utils/authz/Can";
import { dateTimeField, textField } from "../../../../utils/forms/fields";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { dateTimeBeforeToday, numeric, required, validDatetime } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { GenericForm } from "../../components/GenericForm";
import { GET_EVENT_HEADER } from "../EventContent/queries";
import { GET_EVENT_DESCRIPTION, SOLVE_EVENT_MUTATION } from "./queries";

type EventDescriptionProps = RouteComponentProps<{ eventId: string }>;

const eventDescriptionView: React.FC<EventDescriptionProps> = (props: EventDescriptionProps): JSX.Element => {
  const { eventId } = props.match.params;
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("EventDescription", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const [isSolvingModalOpen, setSolvingModalOpen] = React.useState(false);
  const openSolvingModal: (() => void) = (): void => {
    setSolvingModalOpen(true);
  };
  const closeSolvingModal: (() => void) = (): void => {
    setSolvingModalOpen(false);
  };

  const handleErrors: ((error: ApolloError) => void) = (error: ApolloError): void => {
    msgError(translate.t("proj_alerts.error_textsad"));
    rollbar.error("An error occurred loading event description", error);
  };

  const handleDescriptionSubmit: (() => void) = (): void => undefined;

  return (
    <React.StrictMode>
      <Query query={GET_EVENT_DESCRIPTION} variables={{ eventId }} onError={handleErrors}>
        {({ data, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

          const handleUpdateResult: (() => void) = (): void => {
            refetch()
              .catch();
          };

          const handleUpdateError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
            updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
              switch (message) {
                case "Exception - The event has already been closed":
                  msgError(translate.t("project.events.alreadyClosed"));
                  break;
                default:
                  msgError(translate.t("proj_alerts.error_textsad"));
                  rollbar.error("An error occurred updating event", updateError);
              }
            });
          };

          return (
            <React.Fragment>
              <Modal
                footer={<div />}
                headerTitle={translate.t("search_findings.tab_severity.solve")}
                open={isSolvingModalOpen}
              >
                <Mutation
                  mutation={SOLVE_EVENT_MUTATION}
                  onCompleted={handleUpdateResult}
                  onError={handleUpdateError}
                  refetchQueries={[{ query: GET_EVENT_HEADER, variables: { eventId } }]}
                >
                  {(solveEvent: MutationFunction, { loading: submitting }: MutationResult): JSX.Element => {
                    const handleSubmit: ((values: {}) => void) = (values: {}): void => {
                      solveEvent({ variables: { eventId, ...values } })
                        .catch();
                      closeSolvingModal();
                    };

                    return (
                      <GenericForm name="solveEvent" onSubmit={handleSubmit}>
                        {({ pristine }: InjectedFormProps): React.ReactNode => (
                          <React.Fragment>
                            <Row>
                              <Col md={6}>
                                <FormGroup>
                                  <ControlLabel>{translate.t("project.events.description.solved.date")}</ControlLabel>
                                  <Field
                                    component={dateTimeField}
                                    name="date"
                                    validate={[required, validDatetime, dateTimeBeforeToday]}
                                  />
                                </FormGroup>
                              </Col>
                              <Col md={6}>
                                <FormGroup>
                                  <ControlLabel>
                                    {translate.t("project.events.description.solved.affectation")}
                                  </ControlLabel>
                                  <Field
                                    component={textField}
                                    name="affectation"
                                    type="number"
                                    validate={[required, numeric]}
                                  />
                                </FormGroup>
                              </Col>
                            </Row>
                            <ButtonToolbar className="pull-right">
                              <Button bsStyle="success" onClick={closeSolvingModal}>
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
              </Modal>
              <React.Fragment>
                    <GenericForm name="editEvent" initialValues={data.event} onSubmit={handleDescriptionSubmit}>
                      <React.Fragment>
                        <React.Fragment>
                          <Row>
                            <ButtonToolbar className="pull-right">
                              <Can do="backend_api_resolvers_event__do_solve_event">
                                <Button disabled={data.event.eventStatus === "SOLVED"} onClick={openSolvingModal}>
                                  <FluidIcon icon="verified" />&nbsp;{translate.t("search_findings.tab_severity.solve")}
                                </Button>
                              </Can>
                            </ButtonToolbar>
                          </Row>
                          <Row>
                            <Col md={6}>
                              <EditableField
                                alignField="horizontalWide"
                                component={textField}
                                currentValue={data.event.detail}
                                label={translate.t("search_findings.tab_events.description")}
                                name="detail"
                                renderAsEditable={false}
                                type="text"
                              />
                            </Col>
                            <Col md={6}>
                              <EditableField
                                alignField="horizontalWide"
                                component={textField}
                                currentValue={data.event.client}
                                label={translate.t("search_findings.tab_events.client")}
                                name="client"
                                renderAsEditable={false}
                                type="text"
                              />
                            </Col>
                          </Row>
                          <Row>
                            <Col md={6}>
                              <EditableField
                                alignField="horizontalWide"
                                component={textField}
                                currentValue={data.event.analyst}
                                label={translate.t("search_findings.tab_events.analyst")}
                                name="analyst"
                                renderAsEditable={false}
                                type="text"
                              />
                            </Col>
                            <Col md={6}>
                              <EditableField
                                alignField="horizontalWide"
                                component={textField}
                                currentValue={_.isEmpty(data.event.affectation) ? "-" : data.event.affectation}
                                label={translate.t("search_findings.tab_events.affectation")}
                                name="affectation"
                                renderAsEditable={false}
                                type="text"
                              />
                            </Col>
                          </Row>
                          <Row>
                            {!_.isEmpty(data.event.affectedComponents) ? (
                              <Col md={6}>
                                <EditableField
                                  alignField="horizontalWide"
                                  component={textField}
                                  currentValue={data.event.affectedComponents}
                                  label={translate.t("search_findings.tab_events.affected_components")}
                                  name="affectedComponents"
                                  renderAsEditable={false}
                                  type="text"
                                />
                              </Col>
                            ) : undefined}
                            <Col md={6}>
                              <EditableField
                                alignField="horizontalWide"
                                component={textField}
                                currentValue={data.event.accessibility}
                                label={translate.t("search_findings.tab_events.event_in")}
                                name="accessibility"
                                renderAsEditable={false}
                                type="text"
                              />
                            </Col>
                          </Row>
                        </React.Fragment>
                      </React.Fragment>
                    </GenericForm>
              </React.Fragment>
            </React.Fragment>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { eventDescriptionView as EventDescriptionView };
