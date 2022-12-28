import type { IEventAttr } from "./types";

import { castEventStatus, castEventType } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

export const formatTodoEvents: (dataset: IEventAttr[]) => IEventAttr[] = (
  dataset: IEventAttr[]
): IEventAttr[] =>
  dataset.map((event: IEventAttr): IEventAttr => {
    const eventType: string = translate.t(castEventType(event.eventType));
    const eventStatus: string = translate.t(castEventStatus(event.eventStatus));

    return {
      ...event,
      eventStatus,
      eventType,
    };
  });
