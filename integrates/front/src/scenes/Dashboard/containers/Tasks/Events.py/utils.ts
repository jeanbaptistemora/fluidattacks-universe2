/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
