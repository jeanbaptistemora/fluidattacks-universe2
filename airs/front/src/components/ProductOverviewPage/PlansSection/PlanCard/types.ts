/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IPlansCard {
  isMachine: boolean;
  items: {
    check: boolean;
    text: string;
  }[];
  description: string;
  title: string;
}

export type { IPlansCard };
