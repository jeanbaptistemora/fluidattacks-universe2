/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IRootAttr {
  id: string;
  nickname: string;
}

interface IEventAttr {
  closingDate: string;
  detail: string;
  eventDate: string;
  eventStatus: string;
  eventType: string;
  id: string;
  groupName: string;
  root: IRootAttr | null;
}
interface ITodoEvents {
  me: {
    events: IEventAttr[];
  };
}

export type { IEventAttr, ITodoEvents };
