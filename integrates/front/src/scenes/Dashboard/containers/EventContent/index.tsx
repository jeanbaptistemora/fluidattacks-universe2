import type { ApolloError } from "apollo-client";
import { EventCommentsView } from "scenes/Dashboard/containers/EventCommentsView";
import { EventDescriptionView } from "scenes/Dashboard/containers/EventDescriptionView/index";
import { EventEvidenceView } from "scenes/Dashboard/containers/EventEvidenceView";
import { EventHeader } from "scenes/Dashboard/components/EventHeader";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import { NavLink } from "react-router-dom";
import { Query } from "@apollo/react-components";
import type { QueryResult } from "@apollo/react-common";
import React from "react";
import _ from "lodash";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useTabTracking } from "utils/hooks";
import {
  Col100,
  Row,
  Tab,
  TabContent,
  TabsContainer,
} from "styles/styledComponents";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router";

const EventContent: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  // Side effects
  useTabTracking("Event");

  const handleErrors: (error: ApolloError) => void = React.useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred loading event header", error);
      });
    },
    []
  );

  return (
    <React.StrictMode>
      <div>
        <Row>
          <Col100>
            <Query
              onError={handleErrors}
              query={GET_EVENT_HEADER}
              variables={{ eventId }}
            >
              {({ data }: QueryResult): JSX.Element => {
                if (_.isUndefined(data) || _.isEmpty(data)) {
                  return <div />;
                }

                // Eslint annotation needed as the DB handles "any" type
                // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
                const { eventDate, eventStatus, eventType, id } = data.event;

                return (
                  <EventHeader
                    eventDate={eventDate}
                    eventStatus={eventStatus}
                    eventType={eventType}
                    id={id}
                  />
                );
              }}
            </Query>
            <TabsContainer>
              <Tab id={"resourcesTab"}>
                <NavLink
                  activeClassName={"nav-active-bg"}
                  to={`${url}/description`}
                >
                  <i className={"icon pe-7s-note2"} />
                  &nbsp;{translate.t("search_findings.tab_events.description")}
                </NavLink>
              </Tab>
              <Tab id={"evidenceTab"}>
                <NavLink
                  activeClassName={"nav-active-bg"}
                  to={`${url}/evidence`}
                >
                  <i className={"icon pe-7s-note2"} />
                  &nbsp;{translate.t("search_findings.tab_events.evidence")}
                </NavLink>
              </Tab>
              <Tab id={"commentsTab"}>
                <NavLink
                  activeClassName={"nav-active-bg"}
                  to={`${url}/comments`}
                >
                  <i className={"icon pe-7s-comment"} />
                  &nbsp;{translate.t("search_findings.tab_events.comments")}
                </NavLink>
              </Tab>
            </TabsContainer>
            <TabContent>
              <Switch>
                <Route
                  component={EventDescriptionView}
                  exact={true}
                  path={`${path}/description`}
                />
                <Route
                  component={EventEvidenceView}
                  exact={true}
                  path={`${path}/evidence`}
                />
                <Route
                  component={EventCommentsView}
                  exact={true}
                  path={`${path}/comments`}
                />
                <Redirect to={`${path}/description`} />
              </Switch>
            </TabContent>
          </Col100>
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { EventContent };
