/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IVerticalCard {
  alt: string;
  author?: string;
  btnText: string;
  date?: string;
  description: string;
  image: string;
  link: string;
  subtitle?: string;
  title: string;
  width?: string;
  widthMd?: string;
  widthSm?: string;
}

export type { IVerticalCard };
