/* eslint-disable @typescript-eslint/no-unsafe-member-access
-- annotation needed as the DB handles "any" type */
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import { Field } from "redux-form";
import { FluidIcon } from "components/FluidIcon";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import type { InjectedFormProps } from "redux-form";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import React from "react";
import _ from "lodash";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useParams } from "react-router";
import {
  ButtonToolbar,
  Col100,
  Col50,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { DateTime, Text } from "utils/forms/fields";
import {
  GET_EVENT_DESCRIPTION,
  SOLVE_EVENT_MUTATION,
} from "scenes/Dashboard/containers/EventDescriptionView/queries";
import { Mutation, Query } from "@apollo/react-components";
import type {
  MutationFunction,
  MutationResult,
  QueryResult,
} from "@apollo/react-common";
import {
  dateTimeBeforeToday,
  numeric,
  required,
  validDatetime,
} from "utils/validations";

const EventDescriptionView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();

  // State management
  const [isSolvingModalOpen, setSolvingModalOpen] = React.useState(false);
  const openSolvingModal: () => void = React.useCallback((): void => {
    setSolvingModalOpen(true);
  }, []);
  const closeSolvingModal: () => void = React.useCallback((): void => {
    setSolvingModalOpen(false);
  }, []);

  const handleErrors: (error: ApolloError) => void = React.useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred loading event description", error);
      });
    },
    []
  );

  const handleDescriptionSubmit: () => void = React.useCallback(
    (): void => undefined,
    []
  );

  return (
    <React.StrictMode>
      <Query
        onError={handleErrors}
        query={GET_EVENT_DESCRIPTION}
        variables={{ eventId }}
      >
        {({ data, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {
            return <div />;
          }

          const handleUpdateResult: () => void = (): void => {
            void refetch();
          };

          const handleUpdateError: (updateError: ApolloError) => void = (
            updateError: ApolloError
          ): void => {
            updateError.graphQLErrors.forEach(
              ({ message }: GraphQLError): void => {
                switch (message) {
                  case "Exception - The event has already been closed":
                    msgError(translate.t("group.events.alreadyClosed"));
                    break;
                  default:
                    msgError(translate.t("group_alerts.error_textsad"));
                    Logger.warning(
                      "An error occurred updating event",
                      updateError
                    );
                }
              }
            );
          };

          return (
            <React.Fragment>
              <Modal
                headerTitle={translate.t("search_findings.tab_severity.solve")}
                open={isSolvingModalOpen}
              >
                <Mutation
                  mutation={SOLVE_EVENT_MUTATION}
                  onCompleted={handleUpdateResult} // eslint-disable-line react/jsx-no-bind -- Annotation needed due to nested callback
                  onError={handleUpdateError} // eslint-disable-line react/jsx-no-bind
                  refetchQueries={[
                    { query: GET_EVENT_HEADER, variables: { eventId } },
                  ]}
                >
                  {(
                    solveEvent: MutationFunction,
                    { loading: submitting }: MutationResult
                  ): JSX.Element => {
                    const handleSubmit: (
                      values: Record<string, unknown>
                    ) => void = (values: Record<string, unknown>): void => {
                      void solveEvent({ variables: { eventId, ...values } });
                      closeSolvingModal();
                    };

                    return (
                      // eslint-disable-next-line react/jsx-no-bind -- Annotation needed due to nested callback
                      <GenericForm name={"solveEvent"} onSubmit={handleSubmit}>
                        {({ pristine }: InjectedFormProps): React.ReactNode => (
                          <React.Fragment>
                            <Row>
                              <Col50>
                                <FormGroup>
                                  <ControlLabel>
                                    {translate.t(
                                      "group.events.description.solved.date"
                                    )}
                                  </ControlLabel>
                                  <Field
                                    component={DateTime}
                                    name={"date"}
                                    validate={[
                                      required,
                                      validDatetime,
                                      dateTimeBeforeToday,
                                    ]}
                                  />
                                </FormGroup>
                              </Col50>
                              <Col50>
                                <FormGroup>
                                  <ControlLabel>
                                    {translate.t(
                                      "group.events.description.solved.affectation"
                                    )}
                                  </ControlLabel>
                                  <Field
                                    component={Text}
                                    name={"affectation"}
                                    type={"number"}
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
                                  <Button
                                    disabled={pristine || submitting}
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
                    );
                  }}
                </Mutation>
              </Modal>
              <GenericForm
                initialValues={data.event}
                name={"editEvent"}
                onSubmit={handleDescriptionSubmit}
              >
                <div>
                  <div>
                    <Row>
                      <ButtonToolbar>
                        <Can do={"backend_api_mutations_solve_event_mutate"}>
                          <Button
                            disabled={data.event.eventStatus === "SOLVED"}
                            onClick={openSolvingModal}
                          >
                            <FluidIcon icon={"verified"} />
                            &nbsp;
                            {translate.t("search_findings.tab_severity.solve")}
                          </Button>
                        </Can>
                      </ButtonToolbar>
                    </Row>
                    <Row>
                      <Col50>
                        <EditableField
                          alignField={"horizontalWide"}
                          component={Text}
                          currentValue={data.event.detail}
                          label={translate.t(
                            "search_findings.tab_events.description"
                          )}
                          name={"detail"}
                          renderAsEditable={false}
                          type={"text"}
                        />
                      </Col50>
                      <Col50>
                        <EditableField
                          alignField={"horizontalWide"}
                          component={Text}
                          currentValue={data.event.client}
                          label={translate.t(
                            "search_findings.tab_events.client"
                          )}
                          name={"client"}
                          renderAsEditable={false}
                          type={"text"}
                        />
                      </Col50>
                    </Row>
                    <Row>
                      <Col50>
                        <EditableField
                          alignField={"horizontalWide"}
                          component={Text}
                          currentValue={data.event.analyst}
                          label={translate.t(
                            "search_findings.tab_events.analyst"
                          )}
                          name={"analyst"}
                          renderAsEditable={false}
                          type={"text"}
                        />
                      </Col50>
                      <Col50>
                        <EditableField
                          alignField={"horizontalWide"}
                          component={Text}
                          currentValue={
                            _.isEmpty(data.event.affectation)
                              ? "-"
                              : data.event.affectation
                          }
                          label={translate.t(
                            "search_findings.tab_events.affectation"
                          )}
                          name={"affectation"}
                          renderAsEditable={false}
                          type={"text"}
                        />
                      </Col50>
                    </Row>
                    <Row>
                      {!_.isEmpty(data.event.affectedComponents) ? (
                        <Col50>
                          <EditableField
                            alignField={"horizontalWide"}
                            component={Text}
                            currentValue={data.event.affectedComponents}
                            label={translate.t(
                              "search_findings.tab_events.affected_components"
                            )}
                            name={"affectedComponents"}
                            renderAsEditable={false}
                            type={"text"}
                          />
                        </Col50>
                      ) : undefined}
                      <Col50>
                        <EditableField
                          alignField={"horizontalWide"}
                          component={Text}
                          currentValue={data.event.accessibility}
                          label={translate.t(
                            "search_findings.tab_events.event_in"
                          )}
                          name={"accessibility"}
                          renderAsEditable={false}
                          type={"text"}
                        />
                      </Col50>
                    </Row>
                  </div>
                </div>
              </GenericForm>
            </React.Fragment>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { EventDescriptionView };
