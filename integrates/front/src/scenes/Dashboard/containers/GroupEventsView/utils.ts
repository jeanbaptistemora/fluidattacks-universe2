import {
  castEventStatus,
  castEventType,
  formatAccessibility,
} from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

interface IEventConfig {
  accessibility: string;
  eventStatus: string;
  eventType: string;
}

export const formatEvents: (dataset: IEventConfig[]) => IEventConfig[] = (
  dataset: IEventConfig[]
): IEventConfig[] =>
  dataset.map((event: IEventConfig): IEventConfig => {
    const eventType: string = translate.t(castEventType(event.eventType));
    const eventStatus: string = translate.t(castEventStatus(event.eventStatus));
    const accessibility: string = translate.t(
      formatAccessibility(event.accessibility)
    );

    return { ...event, accessibility, eventStatus, eventType };
  });
