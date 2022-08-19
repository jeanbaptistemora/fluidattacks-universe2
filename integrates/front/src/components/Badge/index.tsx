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
    bgColor: "#dbffdb",
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
    color: "#cc8080",
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
