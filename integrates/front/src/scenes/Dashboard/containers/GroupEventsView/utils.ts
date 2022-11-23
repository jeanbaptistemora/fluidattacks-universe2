import _ from "lodash";

import type { IEventAttr, IEventData } from "./types";

import { castEventStatus, castEventType } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

const getEventIndex = (
  selectedEvents: IEventData[],
  allEvents: IEventData[]
): number[] => {
  const selectedIds: string[] = selectedEvents.map(
    (selected: IEventData): string => selected.id
  );

  return allEvents.reduce(
    (
      selectedIndex: number[],
      currentEvent: IEventData,
      currentEventIndex: number
    ): number[] =>
      selectedIds.includes(currentEvent.id)
        ? [...selectedIndex, currentEventIndex]
        : selectedIndex,
    []
  );
};

const getNonSelectableEventIndexToRequestVerification: (
  allEvents: IEventData[]
) => number[] = (allEvents: IEventData[]): number[] => {
  const unsolved = translate.t(castEventStatus("CREATED"));

  return allEvents.reduce(
    (
      selectedEventIndex: number[],
      currentEventData: IEventData,
      currentEventDataIndex: number
    ): number[] =>
      currentEventData.eventStatus === unsolved
        ? selectedEventIndex
        : [...selectedEventIndex, currentEventDataIndex],
    []
  );
};

const formatEvents: (dataset: IEventAttr[]) => IEventData[] = (
  dataset: IEventAttr[]
): IEventData[] =>
  dataset.map((event: IEventAttr): IEventData => {
    const eventType: string = translate.t(castEventType(event.eventType));
    const eventStatus: string = translate.t(castEventStatus(event.eventStatus));

    return {
      ...event,
      eventStatus,
      eventType,
    };
  });

const onSelectSeveralEventsHelper = (
  isSelect: boolean,
  newSelectedEvents: IEventData[],
  currentSelectedEvents: IEventData[],
  setCurrentSelectedEvents: (value: React.SetStateAction<IEventData[]>) => void
): string[] => {
  if (isSelect) {
    const eventsToSet: IEventData[] = Array.from(
      new Set([...currentSelectedEvents, ...newSelectedEvents])
    );
    setCurrentSelectedEvents(eventsToSet);

    return eventsToSet.map((event: IEventData): string => event.id);
  }
  const newSelectedEventIds: string[] = newSelectedEvents.map(
    (event: IEventData): string => event.id
  );
  setCurrentSelectedEvents(
    Array.from(
      new Set(
        currentSelectedEvents.filter(
          (currentSelectedEvent: IEventData): boolean =>
            !newSelectedEventIds.includes(currentSelectedEvent.id)
        )
      )
    )
  );

  return currentSelectedEvents.map((event: IEventData): string => event.id);
};

function formatReattacks(reattacks: string[]): Record<string, string[]> {
  if (reattacks.length > 0) {
    return (
      _.chain(reattacks)
        // CompositeId = "findingId vulnId"
        .groupBy(function getFindingId(compositeId): string {
          // First group by findingId
          return compositeId.split(" ")[0];
        })

        // Then map key-value pairs to look like findingId: [vulnId1, ...]
        .mapValues(function splitIds(compositeArray): string[] {
          return compositeArray.map(
            (compositeId): string => compositeId.split(" ")[1]
          );
        })
        .value()
    );
  }

  return {};
}

export {
  getEventIndex,
  getNonSelectableEventIndexToRequestVerification,
  formatEvents,
  formatReattacks,
  onSelectSeveralEventsHelper,
};
