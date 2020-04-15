/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Redirect, Route, RouteComponentProps, Switch } from "react-router";
import { NavLink } from "react-router-dom";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { EventHeader } from "../../components/EventHeader";
import { EventCommentsView } from "../EventCommentsView";
import { EventDescriptionView } from "../EventDescriptionView/index";
import { EventEvidenceView } from "../EventEvidenceView";
import { default as style } from "../FindingContent/index.css";
import { GET_EVENT_HEADER } from "./queries";

type EventContentProps = RouteComponentProps<{ eventId: string }>;

const eventContent: React.FC<EventContentProps> = (props: EventContentProps): JSX.Element => {
  const { eventId } = props.match.params;

  const handleErrors: ((error: ApolloError) => void) = (error: ApolloError): void => {
    msgError(translate.t("proj_alerts.error_textsad"));
    rollbar.error("An error occurred loading event header", error);
  };

  return (
    <React.StrictMode>
      <React.Fragment>
        <Row>
          <Col md={12} sm={12}>
            <Query query={GET_EVENT_HEADER} variables={{ eventId }} onError={handleErrors}>
              {({ data }: QueryResult): JSX.Element => {
                if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

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
      </React.Fragment>
    </React.StrictMode >
  );
};

export { eventContent as EventContent };
