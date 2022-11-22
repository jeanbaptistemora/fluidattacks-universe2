/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { TSize } from "../Typography/types";

interface ICtaBannerProps {
  button1Link: string;
  button1Text: string;
  button2Link: string;
  button2Text: string;
  title: string;
  paragraph: string;
  image: string;
  matomoAction: string;
  size?: TSize;
  sizeMd?: TSize;
  sizeSm?: TSize;
}

export type { ICtaBannerProps };
