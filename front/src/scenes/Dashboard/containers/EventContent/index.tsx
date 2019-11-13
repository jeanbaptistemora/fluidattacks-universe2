/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import _ from "lodash";
import React from "react";
import { Query, QueryResult } from "react-apollo";
import { Col, Row } from "react-bootstrap";
import { Redirect, Route, RouteComponentProps, Switch } from "react-router";
import { NavLink } from "react-router-dom";
import translate from "../../../../utils/translations/translate";
import { EventHeader } from "../../components/EventHeader";
import { EventCommentsView } from "../EventCommentsView";
import { eventDescriptionView as EventDescriptionView } from "../EventDescriptionView/index";
import { EventEvidenceView } from "../EventEvidenceView";
import style from "../FindingContent/index.css";
import { GET_EVENT_HEADER } from "./queries";

type EventContentProps = RouteComponentProps<{ eventId: string; projectName: string }>;

const eventContent: React.FC<EventContentProps> = (props: EventContentProps): JSX.Element => {
  const { eventId } = props.match.params;

  return (
    <React.StrictMode>
      <div className={style.mainContainer}>
        <Row>
          <Col md={12} sm={12}>
            <Query query={GET_EVENT_HEADER} variables={{ eventId }}>
              {({ data, loading }: QueryResult): JSX.Element => {
                if (_.isUndefined(data) || loading) { return <React.Fragment />; }

                return <EventHeader {...data.event} />;
              }}
            </Query>
            <ul className={style.tabsContainer}>
              <li id="resourcesTab" className={style.tab}>
                <NavLink activeClassName={style.active} to={`${props.match.url}/description`}>
                  <i className="icon pe-7s-note2" />
                  &nbsp;{translate.t("search_findings.tab_events.description")}
                </NavLink>
              </li>
              <li id="evidenceTab" className={style.tab}>
                <NavLink activeClassName={style.active} to={`${props.match.url}/evidence`}>
                  <i className="icon pe-7s-note2" />
                  &nbsp;{translate.t("search_findings.tab_events.evidence")}
                </NavLink>
              </li>
              <li id="commentsTab" className={style.tab}>
                <NavLink activeClassName={style.active} to={`${props.match.url}/comments`}>
                  <i className="icon pe-7s-comment" />
                  &nbsp;{translate.t("search_findings.tab_events.comments")}
                </NavLink>
              </li>
            </ul>
            <div className={style.tabContent}>
              <Switch>
                <Route path={`${props.match.path}/description`} component={EventDescriptionView} exact={true} />
                <Route path={`${props.match.path}/evidence`} component={EventEvidenceView} exact={true} />
                <Route path={`${props.match.path}/comments`} component={EventCommentsView} exact={true} />
                <Redirect to={`${props.match.path}/description`} />
              </Switch>
            </div>
          </Col>
        </Row>
      </div>
    </React.StrictMode >
  );
};

export { eventContent as EventContent };
