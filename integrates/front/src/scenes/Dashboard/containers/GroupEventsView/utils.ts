import _ from "lodash";

import {
  castAffectedComponents,
  castEventStatus,
  castEventType,
  formatAccessibility,
} from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

interface IEventInput {
  accessibility: string[];
  affectedComponents: string;
  eventStatus: string;
  eventType: string;
}
interface IEventConfig {
  accessibility: string;
  affectedComponents: string;
  eventStatus: string;
  eventType: string;
}

const formatEvents: (dataset: IEventInput[]) => IEventConfig[] = (
  dataset: IEventInput[]
): IEventConfig[] =>
  dataset.map((event: IEventInput): IEventConfig => {
    const eventType: string = translate.t(castEventType(event.eventType));
    const eventStatus: string = translate.t(castEventStatus(event.eventStatus));
    const accessibility: string = event.accessibility
      .map((item: string): string => translate.t(formatAccessibility(item)))
      .join(", ");
    const affectedComponents: string = translate.t(
      castAffectedComponents(event.affectedComponents)
    );

    return {
      ...event,
      accessibility,
      affectedComponents,
      eventStatus,
      eventType,
    };
  });

function filterClosingDate(
  rows: IEventConfig[],
  currentDate: string
): IEventConfig[] {
  const selectedDate = new Date(currentDate);

  return rows.filter(
    (row: IEventConfig & { closingDate?: string }): boolean => {
      if (currentDate !== "" && row.closingDate === "-") return false;
      const reportDate = new Date(row.closingDate ?? "");

      return _.isEmpty(currentDate)
        ? true
        : selectedDate.getUTCDate() === reportDate.getUTCDate() &&
            selectedDate.getUTCMonth() === reportDate.getUTCMonth() &&
            selectedDate.getUTCFullYear() === reportDate.getUTCFullYear();
    }
  );
}

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

export type { IEventConfig };
export { filterClosingDate, formatEvents, formatReattacks };
