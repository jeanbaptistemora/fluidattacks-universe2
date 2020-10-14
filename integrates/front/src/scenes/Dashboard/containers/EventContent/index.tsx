/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Redirect, Route, RouteComponentProps, Switch } from "react-router";
import { NavLink } from "react-router-dom";
import { EventHeader } from "scenes/Dashboard/components/EventHeader";
import { EventCommentsView } from "scenes/Dashboard/containers/EventCommentsView";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";
import { EventDescriptionView } from "scenes/Dashboard/containers/EventDescriptionView/index";
import { EventEvidenceView } from "scenes/Dashboard/containers/EventEvidenceView";
import {
  Col100,
  Row,
  Tab,
  TabContent,
  TabsContainer,
} from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

type EventContentProps = RouteComponentProps<{ eventId: string }>;

const eventContent: React.FC<EventContentProps> = (props: EventContentProps): JSX.Element => {
  const { eventId } = props.match.params;

  const handleErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred loading event header", error);
    });
  };

  return (
    <React.StrictMode>
      <React.Fragment>
        <Row>
          <Col100>
            <Query query={GET_EVENT_HEADER} variables={{ eventId }} onError={handleErrors}>
              {({ data }: QueryResult): JSX.Element => {
                if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

                return <EventHeader {...data.event} />;
              }}
            </Query>
            <TabsContainer>
              <Tab id="resourcesTab">
                <NavLink activeClassName={"nav-active-bg"} to={`${props.match.url}/description`}>
                  <i className="icon pe-7s-note2" />
                  &nbsp;{translate.t("search_findings.tab_events.description")}
                </NavLink>
              </Tab>
              <Tab id="evidenceTab">
                <NavLink activeClassName={"nav-active-bg"} to={`${props.match.url}/evidence`}>
                  <i className="icon pe-7s-note2" />
                  &nbsp;{translate.t("search_findings.tab_events.evidence")}
                </NavLink>
              </Tab>
              <Tab id="commentsTab">
                <NavLink activeClassName={"nav-active-bg"} to={`${props.match.url}/comments`}>
                  <i className="icon pe-7s-comment" />
                  &nbsp;{translate.t("search_findings.tab_events.comments")}
                </NavLink>
              </Tab>
            </TabsContainer>
            <TabContent>
              <Switch>
                <Route path={`${props.match.path}/description`} component={EventDescriptionView} exact={true} />
                <Route path={`${props.match.path}/evidence`} component={EventEvidenceView} exact={true} />
                <Route path={`${props.match.path}/comments`} component={EventCommentsView} exact={true} />
                <Redirect to={`${props.match.path}/description`} />
              </Switch>
            </TabContent>
          </Col100>
        </Row>
      </React.Fragment>
    </React.StrictMode >
  );
};

export { eventContent as EventContent };
