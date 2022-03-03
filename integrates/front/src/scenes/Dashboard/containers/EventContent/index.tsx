import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router-dom";

import { EventHeader } from "scenes/Dashboard/components/EventHeader";
import type { IEventHeaderProps } from "scenes/Dashboard/components/EventHeader";
import { EventCommentsView } from "scenes/Dashboard/containers/EventCommentsView";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";
import { EventDescriptionView } from "scenes/Dashboard/containers/EventDescriptionView/index";
import { EventEvidenceView } from "scenes/Dashboard/containers/EventEvidenceView";
import { Tab, TabContent, TabsContainer } from "styles/styledComponents";
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
        <div>
          <div>
            <EventHeader
              eventDate={eventDate}
              eventStatus={eventStatus}
              eventType={eventType}
              id={id}
            />
            <TabsContainer>
              <li>
                <Tab id={"resourcesTab"} to={`${url}/description`}>
                  {translate.t("searchFindings.tabEvents.description")}
                </Tab>
              </li>
              <li>
                <Tab id={"evidenceTab"} to={`${url}/evidence`}>
                  {translate.t("searchFindings.tabEvents.evidence")}
                </Tab>
              </li>
              <li>
                <Tab id={"commentsTab"} to={`${url}/comments`}>
                  {translate.t("searchFindings.tabEvents.comments")}
                </Tab>
              </li>
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
          </div>
        </div>
      </div>
    </React.StrictMode>
  );
};

export { EventContent };
