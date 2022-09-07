/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IEventsDataset } from "..";
import type { IFinding } from "../AffectedReattackAccordion/types";

interface IUpdateAffectedValues {
  eventId: string;
  affectedReattacks: string[];
}

interface IUpdateAffectedModalProps {
  eventsInfo: IEventsDataset | undefined;
  findings: IFinding[];
  onClose: () => void;
  onSubmit: (values: IUpdateAffectedValues) => Promise<void>;
}

export type { IUpdateAffectedValues, IUpdateAffectedModalProps };
