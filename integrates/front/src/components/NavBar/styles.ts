import styled from "styled-components";

type TVariant = "dark" | "light";

interface INavBoxProps {
  variant?: TVariant;
}

interface IVariant {
  bgColor: string;
  borderColor: string;
  color: string;
}

const variants: Record<TVariant, IVariant> = {
  dark: {
    bgColor: "#2e2e38",
    borderColor: "#49495a",
    color: "#e9e9ed",
  },
  light: {
    bgColor: "#f4f4f6",
    borderColor: "#d2d2da",
    color: "#2e2e38",
  },
};

const NavBox = styled.nav.attrs({
  className: "Nav",
})<INavBoxProps>`
  ${({ variant = "dark" }): string => {
    const { bgColor, borderColor, color } = variants[variant];

    return `
      align-items: center;
      background-color: ${bgColor};
      border: 1px solid ${borderColor};
      color: ${color};
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      padding: 4px 20px;
  `;
  }}
`;

const NavHeader = styled.div`
  align-items: center;
  display: flex;
`;

const NavMenu = styled.div`
  align-items: center;
  display: flex;
`;

export type { TVariant };
export { NavBox, NavHeader, NavMenu };
