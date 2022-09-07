/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ICredentialsData } from "../types";

interface ICredentialsModalProps {
  isAdding: boolean;
  isEditing: boolean;
  organizationId: string;
  onClose: () => void;
  selectedCredentials: ICredentialsData[];
  setSelectedCredentials: (selectedCredentials: ICredentialsData[]) => void;
}

export type { ICredentialsModalProps };
