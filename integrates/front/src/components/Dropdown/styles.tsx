import styled from "styled-components";

interface IDropdownContainerProps {
  align: "center" | "left" | "right";
  bgColor: string;
  border: boolean;
  mt?: string;
  shadow: boolean;
  zIndex?: number;
}

const sideMap: Record<IDropdownContainerProps["align"], string> = {
  center: `
    left: 50%;
    transform: translateX(-50%);
  `,
  left: "right: 0;",
  right: "left: 0;",
};

const DropdownContainer = styled.div<IDropdownContainerProps>`
  ${({ align }): string => sideMap[align]}
  background-color: ${({ bgColor }): string => bgColor};
  border: ${({ border }): string => (border ? `1px solid #c7c7d1` : "unset")};
  border-radius: 4px;
  box-shadow: ${({ shadow }): string =>
    shadow ? `0px 0px 6px 3px rgba(0, 0, 0, 0.06)` : "unset"};
  color: #121216;
  display: none;
  margin-top: ${({ mt }): string => (mt === undefined ? "unset" : mt)};
  position: absolute;
  top: 100%;
  z-index: ${({ zIndex = 100 }): number => zIndex};
`;

const Wrapper = styled.div.attrs({
  className: "comp-dropdown",
})`
  display: inline-block;
  position: relative;
  :hover > div {
    display: block;
  }
`;

export type { IDropdownContainerProps };
export { DropdownContainer, Wrapper };
