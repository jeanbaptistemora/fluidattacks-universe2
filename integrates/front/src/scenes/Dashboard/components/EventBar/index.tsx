import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useMemo } from "react";
import { useTranslation } from "react-i18next";

import { GET_ORG_EVENTS } from "./queries";
import type { IEventBarDataset, IEventBarProps, IEventDataset } from "./types";

import { Alert } from "components/Alert";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const EventBar: React.FC<IEventBarProps> = ({
  organizationName,
}: IEventBarProps): JSX.Element => {
  const { t } = useTranslation();

  const { data } = useQuery<IEventBarDataset>(GET_ORG_EVENTS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.warning("An error occurred loading event bar data", error);
        msgError(t("groupAlerts.errorTextsad"));
      });
    },
    variables: { organizationName },
  });

  const events = useMemo(
    (): IEventDataset[] =>
      data === undefined
        ? []
        : data.organizationId.groups.reduce(
            (previousValue: IEventDataset[], currentValue): IEventDataset[] => [
              ...previousValue,
              ...currentValue.events,
            ],
            []
          ),
    [data]
  );
  const openEvents = events.filter(
    (event): boolean => event.eventStatus === "CREATED"
  );
  const hasOpenEvents = openEvents.length > 0;

  const millisecondsInADay = 86400000;
  const oldestDate = hasOpenEvents
    ? new Date(_.sortBy(openEvents, "eventDate")[0].eventDate)
    : new Date();
  const timeInDays = Math.floor(
    (Date.now() - oldestDate.getTime()) / millisecondsInADay
  );
  const eventMessage: string = t("group.events.eventBar", {
    openEvents: openEvents.length,
    timeInDays,
    vulnGroups: Object.keys(_.countBy(openEvents, "groupName")).length,
  });

  return (
    <React.StrictMode>
      <div>
        {hasOpenEvents ? (
          <Alert icon={true} variant={"error"}>
            {eventMessage}
          </Alert>
        ) : undefined}
      </div>
    </React.StrictMode>
  );
};

export { EventBar };
