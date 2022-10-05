/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FC, ReactNode } from "react";
import React from "react";

import type { ICardBoxProps } from "./styles";
import { CardBox, CardImgBox } from "./styles";

import { Text } from "components/Text";

interface ICardProps extends ICardBoxProps {
  children?: ReactNode;
  img?: ReactNode;
  title?: string;
}

const Card: FC<ICardProps> = ({
  children,
  float = false,
  cover = false,
  img,
  onClick,
  title,
}: Readonly<ICardProps>): JSX.Element => (
  <CardBox cover={cover} float={float} onClick={onClick}>
    {img === undefined ? undefined : <CardImgBox>{img}</CardImgBox>}
    {title === undefined ? undefined : (
      <Text fw={7} mb={3} size={"medium"}>
        {title}
      </Text>
    )}
    {children}
  </CardBox>
);

export type { ICardProps };
export { Card };
