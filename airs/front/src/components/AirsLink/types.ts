/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

type TDecorations = "none" | "underline";

interface ILinkProps {
  decoration?: TDecorations;
}

export type { ILinkProps, TDecorations };
