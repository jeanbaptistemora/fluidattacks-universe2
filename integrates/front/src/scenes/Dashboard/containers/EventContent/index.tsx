/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router-dom";

import { Tab, Tabs } from "components/Tabs";
import { EventBar } from "scenes/Dashboard/components/EventBar";
import { EventHeader } from "scenes/Dashboard/components/EventHeader";
import type { IEventHeaderProps } from "scenes/Dashboard/components/EventHeader";
import { EventCommentsView } from "scenes/Dashboard/containers/EventCommentsView";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";
import { EventDescriptionView } from "scenes/Dashboard/containers/EventDescriptionView/index";
import { EventEvidenceView } from "scenes/Dashboard/containers/EventEvidenceView";
import { TabContent } from "styles/styledComponents";
import { useTabTracking } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IEventHeaderData {
  event: IEventHeaderProps;
}

const EventContent: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { eventId, organizationName } =
    useParams<{ eventId: string; organizationName: string }>();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  // Side effects
  useTabTracking("Event");

  const handleErrors = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading event header", error);
      });
    },
    [t]
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
            <EventBar organizationName={organizationName} />
            <EventHeader
              eventDate={eventDate}
              eventStatus={eventStatus}
              eventType={eventType}
              id={id}
            />
            <Tabs>
              <li>
                <Tab id={"resourcesTab"} link={`${url}/description`}>
                  {t("searchFindings.tabEvents.description")}
                </Tab>
              </li>
              <li>
                <Tab id={"evidenceTab"} link={`${url}/evidence`}>
                  {t("searchFindings.tabEvents.evidence")}
                </Tab>
              </li>
              <li>
                <Tab id={"commentsTab"} link={`${url}/comments`}>
                  {t("searchFindings.tabEvents.comments")}
                </Tab>
              </li>
            </Tabs>
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
