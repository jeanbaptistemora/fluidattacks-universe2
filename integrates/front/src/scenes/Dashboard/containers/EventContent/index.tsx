import { useQuery } from "@apollo/react-hooks";
import type { ApolloError } from "apollo-client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router";
import { NavLink } from "react-router-dom";

import { EventHeader } from "scenes/Dashboard/components/EventHeader";
import type { IEventHeaderProps } from "scenes/Dashboard/components/EventHeader";
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
import { useTabTracking } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IEventHeaderData {
  event: IEventHeaderProps;
}

const EventContent: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  // Side effects
  useTabTracking("Event");

  const handleErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading event header", error);
      });
    },
    []
  );

  const { data } = useQuery<IEventHeaderData>(GET_EVENT_HEADER, {
    onError: handleErrors,
    variables: { eventId },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const { eventDate, eventStatus, eventType, id } = data.event;

  return (
    <React.StrictMode>
      <div>
        <Row>
          <Col100>
            <EventHeader
              eventDate={eventDate}
              eventStatus={eventStatus}
              eventType={eventType}
              id={id}
            />
            <TabsContainer>
              <Tab id={"resourcesTab"}>
                <NavLink
                  activeClassName={"nav-active-bg"}
                  to={`${url}/description`}
                >
                  <i className={"icon pe-7s-note2"} />
                  &nbsp;{translate.t("searchFindings.tabEvents.description")}
                </NavLink>
              </Tab>
              <Tab id={"evidenceTab"}>
                <NavLink
                  activeClassName={"nav-active-bg"}
                  to={`${url}/evidence`}
                >
                  <i className={"icon pe-7s-note2"} />
                  &nbsp;{translate.t("searchFindings.tabEvents.evidence")}
                </NavLink>
              </Tab>
              <Tab id={"commentsTab"}>
                <NavLink
                  activeClassName={"nav-active-bg"}
                  to={`${url}/comments`}
                >
                  <i className={"icon pe-7s-comment"} />
                  &nbsp;{translate.t("searchFindings.tabEvents.comments")}
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
