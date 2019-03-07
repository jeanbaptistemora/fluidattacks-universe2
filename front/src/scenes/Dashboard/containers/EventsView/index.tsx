/* tslint:disable:jsx-no-lambda jsx-no-multiline-js no-empty
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import React from "react";
import { Col, Row } from "react-bootstrap";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import translate from "../../../../utils/translations/translate";

export interface IEventsViewProps {
  eventsDataset: Array<{ detail: string; eventDate: string; eventStatus: string; eventType: string; id: string }>;
  onClickRow: ((row: string | undefined) => JSX.Element);
  projectName: string;
}

export const eventsView: React.StatelessComponent<IEventsViewProps> =
  (props: IEventsViewProps): JSX.Element => (
  <React.StrictMode>
    <div id="events" className="tab-pane cont active">
      <Row>
        <Col md={12} sm={12} xs={12}>
          <Row>
            <Col md={12} sm={12} xs={12}>
              <Row>
                <Col md={12} sm={12}>
                  <DataTable
                    dataset={props.eventsDataset}
                    enableRowSelection={false}
                    exportCsv={true}
                    onClickRow={(row: string | undefined): void => {props.onClickRow(row); }}
                    search={true}
                    headers={[
                      {
                        align: "center",
                        dataField: "id",
                        header: translate.t("search_findings.tab_evidence.id"),
                        isDate: false,
                        isStatus: false,
                        width: "12%",
                        wrapped: true,
                      },
                      {
                        align: "center",
                        dataField: "eventDate",
                        header: translate.t("search_findings.tab_evidence.date"),
                        isDate: false,
                        isStatus: false,
                        width: "15%",
                        wrapped: true,
                      },
                      {
                        align: "center",
                        dataField: "detail",
                        header: translate.t("search_findings.tab_evidence.description"),
                        isDate: false,
                        isStatus: false,
                        width: "45%",
                        wrapped: true,
                      },
                      {
                        align: "center",
                        dataField: "eventType",
                        header: translate.t("search_findings.tab_evidence.type"),
                        isDate: false,
                        isStatus: false,
                        width: "25%",
                        wrapped: true,
                      },
                      {
                        align: "center",
                        dataField: "eventStatus",
                        header: translate.t("search_findings.tab_evidence.status"),
                        isDate: false,
                        isStatus: true,
                        width: "13%",
                        wrapped: true,
                      },
                    ]}
                    id="tblEvents"
                    pageSize={15}
                    title=""
                  />
                </Col>
              </Row>
            </Col>
          </Row>
        </Col>
      </Row>
    </div>
  </React.StrictMode>
);
