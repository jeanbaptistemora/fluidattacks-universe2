import styled from "styled-components";

interface IBadgeProps {
  variant: "gray" | "green" | "orange" | "red";
}

interface IVariant {
  bgColor: string;
  color: string;
}

const variants: Record<IBadgeProps["variant"], IVariant> = {
  gray: {
    bgColor: "#e9e9ed",
    color: "#2e2e38",
  },
  green: {
    bgColor: "#c2ffd4",
    color: "#009245",
  },
  orange: {
    bgColor: "#ffebd6",
    color: "#ff961e",
  },
  red: {
    bgColor: "#ffd6d6",
    color: "#bf0b1a",
  },
};

const Badge = styled.span<IBadgeProps>`
  background-color: ${({ variant }): string => variants[variant].bgColor};
  border-radius: 50px;
  color: ${({ variant }): string => variants[variant].color};
  font-weight: 400;
  padding: 4px 12px;
`;

export type { IBadgeProps };
export { Badge };
