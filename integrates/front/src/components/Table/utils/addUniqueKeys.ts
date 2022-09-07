/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

export const addUniqueKeys: (
  dataset: readonly Readonly<Record<string, unknown>>[]
) => Record<string, unknown>[] = (
  dataset: readonly Readonly<Record<string, unknown>>[]
): Record<string, unknown>[] => {
  return dataset.map(
    (
      data: Readonly<Record<string, unknown>>,
      index: number
    ): Record<string, unknown> => {
      return { ...data, uniqueId: index };
    }
  );
};
