/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

type TVariant = "gray" | "green" | "orange" | "red";

interface IBadgeProps {
  variant: TVariant;
}

interface IVariant {
  bgColor: string;
  borderColor: string;
  color: string;
}

const variants: Record<TVariant, IVariant> = {
  gray: {
    bgColor: "#e9e9ed",
    borderColor: "#c7c7d1",
    color: "#2e2e38",
  },
  green: {
    bgColor: "#c2ffd4",
    borderColor: "#afd8b5",
    color: "#009245",
  },
  orange: {
    bgColor: "#ffeecc",
    borderColor: "#ffdca9",
    color: "#d88218",
  },
  red: {
    bgColor: "#fdd8da",
    borderColor: "#fbb1b5",
    color: "#bf0b1a",
  },
};

const Badge = styled.span<IBadgeProps>`
  border-radius: 50px;
  font-weight: 400;
  padding: 4px 12px;
  ${({ variant }): string => {
    const { bgColor, borderColor, color } = variants[variant];

    return `
      background-color: ${bgColor};
      border: 1px solid ${borderColor};
      color: ${color};
    `;
  }}
`;

export type { IBadgeProps };
export { Badge };
