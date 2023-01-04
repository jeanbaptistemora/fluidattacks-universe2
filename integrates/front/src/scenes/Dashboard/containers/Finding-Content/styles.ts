import styled from "styled-components";

type TVariant = "blue" | "gray" | "green" | "orange" | "red" | "redNoBd";

interface ICVSSFContainerProps {
  variant: TVariant;
}

interface IVariant {
  bgColor: string;
  borderColor: string;
  color: string;
}

const variants: Record<TVariant, IVariant> = {
  blue: {
    bgColor: "#dce4f7",
    borderColor: "#3778ff",
    color: "#3778ff",
  },
  gray: {
    bgColor: "#d2d2da",
    borderColor: "#2e2e38",
    color: "#2e2e38",
  },
  green: {
    bgColor: "#c2ffd4",
    borderColor: "#009245",
    color: "#009245",
  },
  orange: {
    bgColor: "#ffeecc",
    borderColor: "#d88218",
    color: "#d88218",
  },
  red: {
    bgColor: "#fdd8da",
    borderColor: "#bf0b1a",
    color: "#bf0b1a",
  },
  redNoBd: {
    bgColor: "#fdd8da",
    borderColor: "#fdd8da",
    color: "#bf0b1a",
  },
};

const ButtonCol = styled.div.attrs({
  className: "flex flex-auto items-center justify-end",
})``;

const TitleContainer = styled.div.attrs({ className: "flex flex-wrap pa3" })`
  background-color: inherit;
`;

const CVSSFContainer = styled.div.attrs({})<ICVSSFContainerProps>`
  div {
    ${({ variant }): string => {
      const { bgColor, borderColor, color } = variants[variant];

      return `
        background-color: ${bgColor};
        border: 1px solid ${borderColor};
        color: ${color};
      `;
    }}
  }
`;
const Title = styled.h1.attrs({ className: "ma0 pa0" })``;

export { ButtonCol, CVSSFContainer, Title, TitleContainer };
