/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Query, QueryResult } from "react-apollo";
import { Col, Row } from "react-bootstrap";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { formatEvents, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { GET_EVENTS } from "./queries";
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

  return (
    <Query query={GET_EVENTS} variables={{ projectName }} onCompleted={handleQryResult}>
      {
        ({ loading, error, data }: QueryResult<IEventsAttr>): React.ReactNode => {
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

            return (
              <React.StrictMode>
                <Row>
                  <Col md={12} sm={12}>
                    <b>{translate.t("search_findings.tab_events.table_advice")}</b>
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
                  </Col>
                </Row>
              </React.StrictMode>
            );
          }
        }}
    </Query>
  );
};

export { projectEventsView as ProjectEventsView };
