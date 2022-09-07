/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

export const GET_EVENT_HEADER: DocumentNode = gql`
  query GetEventHeader($eventId: String!) {
    event(identifier: $eventId) {
      eventDate
      eventStatus
      eventType
      id
    }
  }
`;
