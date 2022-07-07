import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useMemo } from "react";
import { useTranslation } from "react-i18next";

import { GET_ORG_EVENTS } from "./queries";
import type { IEventBarDataset, IEventBarProps } from "./types";

import { Alert } from "components/Alert";
import { TooltipWrapper } from "components/TooltipWrapper";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

type EventDataset = IEventBarDataset["organizationId"]["groups"][0]["events"];

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
    (): EventDataset =>
      data === undefined
        ? []
        : data.organizationId.groups.reduce(
            (previousValue: EventDataset, currentValue): EventDataset => [
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
  const vulnGroups: string[] = Object.keys(_.countBy(openEvents, "groupName"));

  const eventMessage: string = t("group.events.eventBar.message", {
    openEvents: openEvents.length,
    timeInDays,
    vulnGroups: vulnGroups.length,
  });

  const tooltipMessage: string = t("group.events.eventBar.tooltip", {
    groups: vulnGroups.join(", "),
  });

  return (
    <React.StrictMode>
      <div>
        {hasOpenEvents ? (
          <TooltipWrapper id={"eventBarTooltip"} message={tooltipMessage}>
            <Alert icon={true} variant={"error"}>
              {eventMessage}
            </Alert>
          </TooltipWrapper>
        ) : undefined}
      </div>
    </React.StrictMode>
  );
};

export { EventBar };
