import styled from "styled-components";

interface IContainerProps {
  align: "center" | "left" | "right";
}

const sideMap: Record<IContainerProps["align"], string> = {
  center: `
    left: 50%;
    transform: translateX(-50%);
  `,
  left: "right: 0;",
  right: "left: 0;",
};

const Wrapper = styled.div`
  display: inline-block;
  position: relative;
  :hover > div {
    display: block;
  }
`;

const Container = styled.div<IContainerProps>`
  ${({ align }): string => sideMap[align]}
  background-color: #e9e9ed;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
  display: none;
  min-width: 240px;
  padding: 8px;
  position: absolute;
  top: 100%;
`;

export type { IContainerProps };
export { Wrapper, Container };
