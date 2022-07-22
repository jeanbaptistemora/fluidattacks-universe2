import _ from "lodash";

import type { IEventAttr, IEventData } from "./types";

import {
  castAffectedComponents,
  castEventStatus,
  castEventType,
  formatAccessibility,
} from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

const formatEvents: (dataset: IEventAttr[]) => IEventData[] = (
  dataset: IEventAttr[]
): IEventData[] =>
  dataset.map((event: IEventAttr): IEventData => {
    const eventType: string = translate.t(castEventType(event.eventType));
    const eventStatus: string = translate.t(castEventStatus(event.eventStatus));
    const accessibility: string = event.accessibility
      .map((item: string): string => translate.t(formatAccessibility(item)))
      .join(", ");
    const affectedComponents: string = event.affectedComponents
      .map((item: string): string => translate.t(castAffectedComponents(item)))
      .join(", ");

    return {
      ...event,
      accessibility,
      affectedComponents,
      eventStatus,
      eventType,
    };
  });

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

export { getEventIndex, formatEvents, formatReattacks };
