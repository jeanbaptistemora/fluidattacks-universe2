/* tslint:disable jsx-no-multiline-js
 * Disabling this rule is necessary for the sake of readability
 * of the code that renders the timeline items
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React, { ComponentType } from "react";
import { Col, Row } from "react-bootstrap";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import store from "../../../../store/index";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import { TrackingItem } from "../../components/TrackingItem";
import { VulnerabilitiesView } from "../../components/Vulnerabilities/index";
import * as actions from "./actions";
import { default as style } from "./index.css";

export interface ITrackingViewProps {
  closings: IClosing[];
  findingId: string;
  userRole: string;
}

export interface IClosing {
  closed: number;
  cycle: number;
  date: string;
  effectiveness: number;
  open: number;
}

const mapStateToProps: ((arg1: StateType<Reducer>) => ITrackingViewProps) =
  (state: StateType<Reducer>): ITrackingViewProps =>
  ({
    ...state,
    closings: state.dashboard.tracking.closings,
  });

export const trackingViewComponent: React.FC<ITrackingViewProps> = (props: ITrackingViewProps): JSX.Element => {
  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingTracking", {
      Organization: (window as Window & { userOrganization: string }).userOrganization,
      User: (window as Window & { userName: string }).userName,
    });
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );
    thunkDispatch(actions.loadTracking(props.findingId));
  };
  React.useEffect(onMount, []);

  return (
    <React.StrictMode>
        <React.Fragment>
          <Row>
            <Col md={12}>
              { _.includes(["admin", "analyst"], props.userRole) ?
              <Row>
                <Col md={2} className={style.text_right}>
                  <label className={style.track_title}>{translate.t("search_findings.tab_tracking.pending")}</label>
                </Col>
                <Col md={10}>
                  <VulnerabilitiesView
                    analyst={_.includes(["admin", "analyst"], props.userRole)}
                    editMode={false}
                    editModePending={true}
                    state={"PENDING"}
                    findingId={props.findingId}
                    userRole={props.userRole}
                  />
                </Col>
              </Row>
              : undefined }
              <Row>
                <Col md={2} className={style.text_right}>
                  <label className={style.track_title}>{translate.t("search_findings.tab_tracking.open")}</label>
                </Col>
                <Col md={10}>
                  <VulnerabilitiesView
                    analyst={_.includes(["admin", "analyst"], props.userRole)}
                    editMode={false}
                    findingId={props.findingId}
                    state={"open"}
                    userRole={props.userRole}
                  />
                </Col>
              </Row>
              <Row>
                <Col md={2} className={style.text_right}>
                  <label className={style.track_title}>{translate.t("search_findings.tab_tracking.closed")}</label>
                </Col>
                <Col md={10}>
                  <VulnerabilitiesView
                    analyst={_.includes(["admin", "analyst"], props.userRole)}
                    editMode={false}
                    findingId={props.findingId}
                    state={"closed"}
                    userRole={props.userRole}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
        <Row>
          <Col mdOffset={3} md={9} sm={12}>
            <ul className={style.timelineContainer}>
              {props.closings.map((closing: IClosing, index: number): JSX.Element => (
                <TrackingItem
                  closed={closing.closed}
                  date={closing.date}
                  effectiveness={closing.effectiveness}
                  isRoot={index === 0}
                  key={index}
                  open={closing.open}
                />
              ))}
            </ul>
          </Col>
        </Row>
      </React.Fragment>
    </React.StrictMode>
  );
};

export const trackingView: ComponentType<ITrackingViewProps> = reduxWrapper
(
  trackingViewComponent,
  mapStateToProps,
);
