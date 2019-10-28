/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { Modal } from "../../../../components/Modal";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { formatEvents, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { GenericForm } from "../../components/GenericForm";
import { CREATE_EVENT_MUTATION, GET_EVENTS } from "./queries";
import { IEventsAttr, IEventViewBaseProps } from "./types";

const tableHeaders: IHeader[] = [
  {
    align: "center", dataField: "id", header: translate.t("search_findings.tab_events.id"), isDate: false,
    isStatus: false, width: "12%", wrapped: true,
  },
  {
    align: "center", dataField: "eventDate", header: translate.t("search_findings.tab_events.date"), isDate: false,
    isStatus: false, width: "15%", wrapped: true,
  },
  {
    align: "center", dataField: "detail", header: translate.t("search_findings.tab_events.description"), isDate: false,
    isStatus: false, width: "45%", wrapped: true,
  },
  {
    align: "center", dataField: "eventType", header: translate.t("search_findings.tab_events.type"), isDate: false,
    isStatus: false, width: "25%", wrapped: true,
  },
  {
    align: "center", dataField: "eventStatus", header: translate.t("search_findings.tab_events.status"), isDate: false,
    isStatus: true, width: "13%", wrapped: true,
  },
];
const projectEventsView: React.FunctionComponent<IEventViewBaseProps> = (props: IEventViewBaseProps): JSX.Element => {
  const { projectName } = props.match.params;
  const handleQryResult: ((qrResult: IEventsAttr) => void) = (qrResult: IEventsAttr): void => {
    mixpanel.track("ProjectEvents", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
    hidePreloader();
  };

  const goToEvent: ((rowInfo: { id: string }) => void) = (rowInfo: { id: string }): void => {
    mixpanel.track("ReadEvent", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
    location.hash = `#!/project/${projectName}/events/${rowInfo.id}/description`;
  };

  const [isEventModalOpen, setEventModalOpen] = React.useState(false);

  const openNewEventModal: (() => void) = (): void => {
    setEventModalOpen(true);
  };

  const closeNewEventModal: (() => void) = (): void => {
    setEventModalOpen(false);
  };

  return (
    <Query query={GET_EVENTS} variables={{ projectName }} onCompleted={handleQryResult}>
      {
        ({ data, error, loading, refetch }: QueryResult<IEventsAttr>): React.ReactNode => {
          if (loading) {
            showPreloader();

            return <React.Fragment />;
          }
          if (!_.isUndefined(error)) {
            hidePreloader();
            handleGraphQLErrors("An error occurred getting eventualities", error);

            return <React.Fragment />;
          }
          if (!_.isUndefined(data)) {
            const handleMutationResult: ((result: { createEvent: { success: boolean } }) => void) = (
              result: { createEvent: { success: boolean } },
            ): void => {
              if (result.createEvent.success) {
                closeNewEventModal();
                msgSuccess(
                  translate.t("project.events.success_create"),
                  translate.t("project.events.title_success"),
                );
                refetch()
                  .catch();
              }
            };

            return (
              <React.StrictMode>
                <Row>
                  <Col md={2} mdOffset={5}>
                    <ButtonToolbar>
                      {(window as typeof window & { userRole: string }).userRole === "admin"
                        ? <Button onClick={openNewEventModal}>
                          <Glyphicon glyph="plus" />&nbsp;{translate.t("project.events.new")}
                        </Button>
                        : undefined}
                    </ButtonToolbar>
                  </Col>
                </Row>
                <Modal
                  footer={<div />}
                  headerTitle={translate.t("project.events.new")}
                  onClose={closeNewEventModal}
                  open={isEventModalOpen}
                >
                  <Mutation mutation={CREATE_EVENT_MUTATION} onCompleted={handleMutationResult}>
                    {(createEvent: MutationFn, { loading: submitting }: MutationResult): React.ReactNode => {
                      const handleSubmit: ((values: {}) => void) = (values: {}): void => {
                        createEvent({ variables: { projectName, ...values } })
                          .catch();
                      };

                      return (
                        <GenericForm name="newEvent" onSubmit={handleSubmit}>
                          {({ pristine }: InjectedFormProps): JSX.Element => (
                            <React.Fragment>
                              <Row />
                              <br />
                              <ButtonToolbar className="pull-right">
                                <Button bsStyle="success" onClick={closeNewEventModal}>
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
                <p>{translate.t("search_findings.tab_events.table_advice")}</p>
                <DataTable
                  dataset={formatEvents(data.project.events)}
                  enableRowSelection={false}
                  exportCsv={true}
                  onClickRow={goToEvent}
                  search={true}
                  headers={tableHeaders}
                  id="tblEvents"
                  pageSize={15}
                  title=""
                  selectionMode="none"
                />
              </React.StrictMode>
            );
          }
        }}
    </Query>
  );
};

export { projectEventsView as ProjectEventsView };
