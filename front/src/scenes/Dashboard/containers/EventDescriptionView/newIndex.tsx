/* tslint:disable:jsx-no-multiline-js
 * Disabling this rule is necessary for accessing render props from apollo components
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { numeric, required } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { GenericForm } from "../../components/GenericForm";
import { GET_EVENT_DESCRIPTION, UPDATE_DESCRIPTION_MUTATION } from "./queries";

type EventDescriptionProps = RouteComponentProps<{ eventId: string; projectName: string }>;

const eventDescriptionView: React.FC<EventDescriptionProps> = (props: EventDescriptionProps): JSX.Element => {
  const { eventId } = props.match.params;
  const { userName, userOrganization, userRole } = (window as typeof window & {
    userName: string; userOrganization: string; userRole: string;
  });

  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  const onMount: (() => void) = (): void => {
    mixpanel.track("EventDescription", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  return (
    <React.StrictMode>
      <Query query={GET_EVENT_DESCRIPTION} variables={{ eventId }}>
        {({ data, loading, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }

          const handleUpdateResult: (() => void) = (): void => {
            hidePreloader();
            refetch()
              .catch();
          };

          const canEdit: boolean = _.includes(["admin", "analyst"], userRole) && data.event.eventStatus !== "CLOSED";

          return (
            <React.Fragment>
              <Mutation mutation={UPDATE_DESCRIPTION_MUTATION} onCompleted={handleUpdateResult}>
                {(updateDescription: MutationFn, { loading: submitting }: MutationResult): React.ReactNode => {
                  const handleSubmit: ((values: { [key: string]: string }) => void) = (
                    values: { [key: string]: string },
                  ): void => {
                    showPreloader();
                    updateDescription({ variables: { eventId, ...values } })
                      .catch();
                    setEditing(false);
                  };

                  return (
                    <GenericForm name="editEvent" initialValues={data.event} onSubmit={handleSubmit}>
                      {({ pristine }: InjectedFormProps): React.ReactNode => (
                        <React.Fragment>
                          <Row>
                            <ButtonToolbar className="pull-right">
                              {isEditing ? (
                                <Button disabled={pristine || submitting} type="submit">
                                  <FluidIcon icon="loading" />&nbsp;{translate.t("search_findings.tab_severity.update")}
                                </Button>
                              ) : undefined}
                              {canEdit ? (
                                <Button onClick={handleEditClick}>
                                  <FluidIcon icon="edit" />&nbsp;{translate.t("search_findings.tab_severity.editable")}
                                </Button>
                              ) : undefined}
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
                                renderAsEditable={isEditing}
                                type="text"
                                validate={[numeric, required]}
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
                      )}
                    </GenericForm>
                  );
                }}
              </Mutation>
            </React.Fragment>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { eventDescriptionView as EventDescriptionView };
