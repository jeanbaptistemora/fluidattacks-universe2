/* tslint:disable:jsx-no-lambda jsx-no-multiline-js no-empty
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import React, { ComponentType } from "react";
import { Col, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import {
  InferableComponentEnhancer,
  lifecycle,
} from "recompose";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import store from "../../../../store/index";
import { castEventStatus, castEventType } from "../../../../utils/formatHelpers";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import * as actions from "./actions";

type IEventViewBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

interface IEventsViewStateProps extends RouteComponentProps  {
  eventsDataset: Array<{ detail: string; eventDate: string; eventStatus: string; eventType: string; id: string }>;
  onClickRow: ((row: string | undefined) => JSX.Element);
  projectName: string;
}

export type IEventsViewProps = IEventViewBaseProps & IEventsViewStateProps;

const enhance: InferableComponentEnhancer<{}> =
lifecycle<IEventsViewProps, {}>({
  componentWillUnmount(): void { store.dispatch(actions.clearEventsState()); },
  componentDidMount(): void {
    const { projectName } =  this.props.match.params;
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );
    thunkDispatch(actions.loadEvents(projectName));
  },
});

const mapStateToProps: ((arg1: StateType<Reducer>) => IEventsViewProps) =
  (state: StateType<Reducer>): IEventsViewProps => ({
    ...state,
    eventsDataset: state.dashboard.events.eventsDataset,
  }
);

export const component: React.StatelessComponent<IEventsViewProps> =
  (props: IEventsViewProps): JSX.Element => {
      props.eventsDataset = props.eventsDataset.map((row: IEventsViewProps["eventsDataset"][0]) => {
        row.eventType = translate.t(castEventType(row.eventType));
        row.eventStatus = translate.t(castEventStatus(row.eventStatus));

        return row;
      });

      return (
  <React.StrictMode>
    <div id="events" className="tab-pane cont active">
      <Row>
        <Col md={12} sm={12} xs={12}>
          <b>{translate.t("search_findings.tab_events.table_advice")}</b>
          <Row>
            <Col md={12} sm={12} xs={12}>
              <Row>
                <Col md={12} sm={12}>
                  <DataTable
                    dataset={props.eventsDataset}
                    enableRowSelection={false}
                    exportCsv={true}
                    onClickRow={(row: { id: string }): void => {
                      window.location.href =
                      `/integrates/dashboard#!/project/${props.projectName}/events/${row.id}/description`;
                    }}
                    search={true}
                    headers={[
                      {
                        align: "center",
                        dataField: "id",
                        header: translate.t("search_findings.tab_events.id"),
                        isDate: false,
                        isStatus: false,
                        width: "12%",
                        wrapped: true,
                      },
                      {
                        align: "center",
                        dataField: "eventDate",
                        header: translate.t("search_findings.tab_events.date"),
                        isDate: false,
                        isStatus: false,
                        width: "15%",
                        wrapped: true,
                      },
                      {
                        align: "center",
                        dataField: "detail",
                        header: translate.t("search_findings.tab_events.description"),
                        isDate: false,
                        isStatus: false,
                        width: "45%",
                        wrapped: true,
                      },
                      {
                        align: "center",
                        dataField: "eventType",
                        header: translate.t("search_findings.tab_events.type"),
                        isDate: false,
                        isStatus: false,
                        width: "25%",
                        wrapped: true,
                      },
                      {
                        align: "center",
                        dataField: "eventStatus",
                        header: translate.t("search_findings.tab_events.status"),
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
); };

export const eventsView: ComponentType<IEventsViewProps> = reduxWrapper
(
  enhance(component) as React.StatelessComponent<IEventsViewProps>,
  mapStateToProps,
);
