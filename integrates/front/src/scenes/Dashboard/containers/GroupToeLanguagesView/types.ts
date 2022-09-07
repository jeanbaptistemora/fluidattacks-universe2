/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface ICodeLanguage {
  language: string;
  loc: number;
  percentage?: number;
}

export type { ICodeLanguage };
