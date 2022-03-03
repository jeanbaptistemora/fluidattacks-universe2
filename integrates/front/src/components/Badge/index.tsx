import styled from "styled-components";

interface IBadgeProps {
  variant: "gray" | "green" | "orange" | "red";
}

interface IVariant {
  backgroundColor: string;
  color: string;
}

const variants: Record<IBadgeProps["variant"], IVariant> = {
  gray: {
    backgroundColor: "#e9e9ed",
    color: "#2e2e38",
  },
  green: {
    backgroundColor: "#c2ffd4",
    color: "#009245",
  },
  orange: {
    backgroundColor: "#ffebd6",
    color: "#ff961e",
  },
  red: {
    backgroundColor: "#ffd6d6",
    color: "#ff3435",
  },
};

const Badge = styled.span<IBadgeProps>`
  background-color: ${(props): string =>
    variants[props.variant].backgroundColor};
  border-radius: 50px;
  color: ${(props): string => variants[props.variant].color};
  font-weight: 400;
  padding: 4px 12px;
`;

export { Badge, IBadgeProps };
