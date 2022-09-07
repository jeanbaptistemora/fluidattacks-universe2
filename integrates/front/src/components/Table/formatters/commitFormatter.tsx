/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

export function commitFormatter(value: string): string {
  const COMMIT_LENGTH: number = 7;

  return value.slice(0, COMMIT_LENGTH);
}
