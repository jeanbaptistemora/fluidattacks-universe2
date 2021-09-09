import _ from "lodash";

import {
  castActionBeforeBlocking,
  castAffectedComponents,
  castEventStatus,
  castEventType,
  formatAccessibility,
} from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

interface IEventConfig {
  accessibility: string;
  actionAfterBlocking: string;
  actionBeforeBlocking: string;
  affectedComponents: string;
  eventStatus: string;
  eventType: string;
}

const formatEvents: (dataset: IEventConfig[]) => IEventConfig[] = (
  dataset: IEventConfig[]
): IEventConfig[] =>
  dataset.map((event: IEventConfig): IEventConfig => {
    const eventType: string = translate.t(castEventType(event.eventType));
    const eventStatus: string = translate.t(castEventStatus(event.eventStatus));
    const accessibility: string = translate.t(
      formatAccessibility(event.accessibility)
    );
    const affectedComponents: string = translate.t(
      castAffectedComponents(event.affectedComponents)
    );
    const actionBeforeBlocking: string = translate.t(
      castActionBeforeBlocking(event.actionBeforeBlocking)
    );

    return {
      ...event,
      accessibility,
      actionBeforeBlocking,
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

export { filterClosingDate, formatEvents, IEventConfig };
