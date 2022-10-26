/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ITypographyProps, TWeight } from "../types";

interface ITextProps extends ITypographyProps {
  children: React.ReactNode;
  weight?: TWeight;
}

export type { ITextProps };
