/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ICredentialsData } from "../types";

interface IActionButtonsProps {
  isAdding: boolean;
  isEditing: boolean;
  isRemoving: boolean;
  onAdd: () => void;
  onEdit: () => void;
  onRemove: () => void;
  selectedCredentials: ICredentialsData | undefined;
}

export type { IActionButtonsProps };
