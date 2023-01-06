import styled from "styled-components";

type TVariant = "deepRed" | "none" | "orange" | "red" | "yellow";

interface ITagProps {
  variant: TVariant;
}

interface IVariant {
  bgColor: string;
}

const variants: Record<TVariant, IVariant> = {
  deepRed: {
    bgColor: "#b3000f",
  },
  none: {
    bgColor: "#d2d2da",
  },
  orange: {
    bgColor: "#fc9117",
  },
  red: {
    bgColor: "#f2182a",
  },
  yellow: {
    bgColor: "#ffce00",
  },
};

const Tag = styled.div`
  display: inline-block;
`;

const NumberDisplay = styled.div<ITagProps>`
  display: inline-block;
  padding: 2px 8px;
  border-radius: inherit;
  border-radius: 5px;
  border-top-right-radius: 0px;
  border-bottom-right-radius: 0px;
  background-color: white;
  color: #2e2e38;
  text-align: center;

  ${({ variant }): string => {
    const { bgColor } = variants[variant];

    return `
      border: 1px solid ${bgColor};
    `;
  }}
`;

const VulnDisplay = styled.div<ITagProps>`
  display: inline-block;
  padding: 2px 8px;
  border-radius: 5px;
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
  background-color: white;
  text-align: center;
  color: #fff;
  font-weight: 400;

  ${({ variant }): string => {
    const { bgColor } = variants[variant];

    return `
      background-color: ${bgColor};
      border: 1px solid ${bgColor};
    `;
  }}
`;

export { NumberDisplay, Tag, VulnDisplay };
export type { ITagProps };
