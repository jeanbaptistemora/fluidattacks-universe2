import styled from "styled-components";

interface IDropdownContainerProps {
  align: "center" | "left" | "right";
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
  background-color: #e9e9ed;
  border: 1px solid #c7c7d1;
  border-radius: 4px;
  display: none;
  position: absolute;
  top: 100%;
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
