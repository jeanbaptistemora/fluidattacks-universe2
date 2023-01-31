import styled from "styled-components";

interface IAccordionHeaderProps {
  collapsed: boolean;
  iconSide: "left" | "right";
}

const AccordionContainer = styled.div.attrs({
  className: "comp-accordion",
})``;

const AccordionHeader = styled.div<IAccordionHeaderProps>`
  ${({ collapsed }): string => `
    border: 1px solid ${collapsed ? "#c7c7d1" : "#a5a5b6"};

    > .ico-collapse {
      transform: rotate(${collapsed ? 180 : 0}deg);
    }
  `}
  align-items: center;
  background-color: #e9e9ed;
  color: #121216;
  display: flex;
  ${({ iconSide }): string => {
    const isRight = iconSide === "right";

    return `
      flex-direction: row${isRight ? "-reverse" : ""};
      justify-content: ${isRight ? "space-between" : "flex-start"};
    `;
  }}
  margin-bottom: 8px;
  transition: all 0.3s ease;

  :hover {
    background-color: #c7c7d1;
  }

  > * {
    margin: 16px;
  }
`;

const IconWrapper = styled.span.attrs({
  className: "ico-collapse",
})`
  color: #65657b;
  display: inline-block;
  transition: transform 0.3s ease;
`;

export type { IAccordionHeaderProps };
export { AccordionContainer, AccordionHeader, IconWrapper };
