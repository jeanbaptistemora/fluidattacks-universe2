/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for accessing render props from apollo components
 */
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useParams } from "react-router";
import { Field, InjectedFormProps } from "redux-form";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { Modal } from "components/Modal";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";
import {
  GET_EVENT_DESCRIPTION,
  SOLVE_EVENT_MUTATION,
} from "scenes/Dashboard/containers/EventDescriptionView/queries";
import {
  ButtonToolbar,
  Col100,
  Col50,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { DateTime, Text } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { dateTimeBeforeToday, numeric, required, validDatetime } from "utils/validations";

const eventDescriptionView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();

  // State management
  const [isSolvingModalOpen, setSolvingModalOpen] = React.useState(false);
  const openSolvingModal: (() => void) = (): void => {
    setSolvingModalOpen(true);
  };
  const closeSolvingModal: (() => void) = (): void => {
    setSolvingModalOpen(false);
  };

  const handleErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred loading event description", error);
    });
  };

  const handleDescriptionSubmit: (() => void) = (): void => undefined;

  return (
    <React.StrictMode>
      <Query query={GET_EVENT_DESCRIPTION} variables={{ eventId }} onError={handleErrors}>
        {({ data, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

          const handleUpdateResult: (() => void) = (): void => {
            void refetch();
          };

          const handleUpdateError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
            updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
              switch (message) {
                case "Exception - The event has already been closed":
                  msgError(translate.t("group.events.alreadyClosed"));
                  break;
                default:
                  msgError(translate.t("group_alerts.error_textsad"));
                  Logger.warning("An error occurred updating event", updateError);
              }
            });
          };

          return (
            <React.Fragment>
              <Modal
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
                      void solveEvent({ variables: { eventId, ...values } });
                      closeSolvingModal();
                    };

                    return (
                      <GenericForm name="solveEvent" onSubmit={handleSubmit}>
                        {({ pristine }: InjectedFormProps): React.ReactNode => (
                          <React.Fragment>
                            <Row>
                              <Col50>
                                <FormGroup>
                                  <ControlLabel>{translate.t("group.events.description.solved.date")}</ControlLabel>
                                  <Field
                                    component={DateTime}
                                    name="date"
                                    validate={[required, validDatetime, dateTimeBeforeToday]}
                                  />
                                </FormGroup>
                              </Col50>
                              <Col50>
                                <FormGroup>
                                  <ControlLabel>
                                    {translate.t("group.events.description.solved.affectation")}
                                  </ControlLabel>
                                  <Field
                                    component={Text}
                                    name="affectation"
                                    type="number"
                                    validate={[required, numeric]}
                                  />
                                </FormGroup>
                              </Col50>
                            </Row>
                            <hr />
                            <Row>
                              <Col100>
                                <ButtonToolbar>
                                  <Button onClick={closeSolvingModal}>
                                    {translate.t("confirmmodal.cancel")}
                                  </Button>
                                  <Button type="submit" disabled={pristine || submitting}>
                                    {translate.t("confirmmodal.proceed")}
                                  </Button>
                                </ButtonToolbar>
                              </Col100>
                            </Row>
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
                            <ButtonToolbar>
                              <Can do="backend_api_mutations_solve_event_mutate">
                                <Button disabled={data.event.eventStatus === "SOLVED"} onClick={openSolvingModal}>
                                  <FluidIcon icon="verified" />&nbsp;{translate.t("search_findings.tab_severity.solve")}
                                </Button>
                              </Can>
                            </ButtonToolbar>
                          </Row>
                          <Row>
                            <Col50>
                              <EditableField
                                alignField="horizontalWide"
                                component={Text}
                                currentValue={data.event.detail}
                                label={translate.t("search_findings.tab_events.description")}
                                name="detail"
                                renderAsEditable={false}
                                type="text"
                              />
                            </Col50>
                            <Col50>
                              <EditableField
                                alignField="horizontalWide"
                                component={Text}
                                currentValue={data.event.client}
                                label={translate.t("search_findings.tab_events.client")}
                                name="client"
                                renderAsEditable={false}
                                type="text"
                              />
                            </Col50>
                          </Row>
                          <Row>
                            <Col50>
                              <EditableField
                                alignField="horizontalWide"
                                component={Text}
                                currentValue={data.event.analyst}
                                label={translate.t("search_findings.tab_events.analyst")}
                                name="analyst"
                                renderAsEditable={false}
                                type="text"
                              />
                            </Col50>
                            <Col50>
                              <EditableField
                                alignField="horizontalWide"
                                component={Text}
                                currentValue={_.isEmpty(data.event.affectation) ? "-" : data.event.affectation}
                                label={translate.t("search_findings.tab_events.affectation")}
                                name="affectation"
                                renderAsEditable={false}
                                type="text"
                              />
                            </Col50>
                          </Row>
                          <Row>
                            {!_.isEmpty(data.event.affectedComponents) ? (
                              <Col50>
                                <EditableField
                                  alignField="horizontalWide"
                                  component={Text}
                                  currentValue={data.event.affectedComponents}
                                  label={translate.t("search_findings.tab_events.affected_components")}
                                  name="affectedComponents"
                                  renderAsEditable={false}
                                  type="text"
                                />
                              </Col50>
                            ) : undefined}
                            <Col50>
                              <EditableField
                                alignField="horizontalWide"
                                component={Text}
                                currentValue={data.event.accessibility}
                                label={translate.t("search_findings.tab_events.event_in")}
                                name="accessibility"
                                renderAsEditable={false}
                                type="text"
                              />
                            </Col50>
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
