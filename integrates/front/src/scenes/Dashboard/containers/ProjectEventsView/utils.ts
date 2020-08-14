import translate from "../../../../utils/translations/translate";
import {
  castEventStatus,
  castEventType,
} from "../../../../utils/formatHelpers";

interface IEventConfig {
  eventStatus: string;
  eventType: string;
}

export const formatEvents: (dataset: IEventConfig[]) => IEventConfig[] = (
  dataset: IEventConfig[]
): IEventConfig[] =>
  dataset.map(
    (event: IEventConfig): IEventConfig => {
      const eventType: string = translate.t(castEventType(event.eventType));
      const eventStatus: string = translate.t(
        castEventStatus(event.eventStatus)
      );

      return { ...event, eventStatus, eventType };
    }
  );
