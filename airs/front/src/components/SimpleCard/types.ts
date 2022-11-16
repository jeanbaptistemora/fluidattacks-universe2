/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface ISimpleCardProps {
  bgColor?: string;
  borderColor?: string;
  description: string;
  descriptionColor: string;
  image: string;
  title?: string;
  titleColor?: string;
  titleMinHeight?: string;
  width?: string;
  widthMd?: string;
  widthSm?: string;
}

export type { ISimpleCardProps };
