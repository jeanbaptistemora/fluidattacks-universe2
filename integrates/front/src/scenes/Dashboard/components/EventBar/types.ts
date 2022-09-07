/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IEventBarDataset {
  organizationId: {
    id: string;
    groups: {
      events: {
        eventDate: string;
        eventStatus: string;
        groupName: string;
      }[];
      name: string;
    }[];
    name: string;
  };
}

interface IEventBarProps {
  organizationName: string;
}

export type { IEventBarDataset, IEventBarProps };
