/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ICredentialsData } from "./types";

const getCredentialsIndex = (
  selectedCredentials: ICredentialsData[],
  allCredentials: ICredentialsData[]
): number[] => {
  const selectedIds: string[] = selectedCredentials.map(
    (selected: ICredentialsData): string => selected.id
  );

  return allCredentials.reduce(
    (
      selectedIndex: number[],
      currentCredentials: ICredentialsData,
      currentCredentialsIndex: number
    ): number[] =>
      selectedIds.includes(currentCredentials.id)
        ? [...selectedIndex, currentCredentialsIndex]
        : selectedIndex,
    []
  );
};

export { getCredentialsIndex };
