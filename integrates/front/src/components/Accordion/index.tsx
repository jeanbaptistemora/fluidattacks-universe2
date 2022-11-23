import { faAngleUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ReactNode } from "react";
import React, { useCallback, useState } from "react";

import type { IAccordionHeaderProps } from "./styles";
import { AccordionContainer, AccordionHeader, IconWrapper } from "./styles";

import type { IContainerProps } from "components/Container";
import { Container } from "components/Container";

interface IAccordionProps extends IContainerProps {
  children: ReactNode;
  header: ReactNode;
  iconSide?: IAccordionHeaderProps["iconSide"];
  initCollapsed?: boolean;
}

const Accordion: React.FC<IAccordionProps> = ({
  children,
  header,
  height,
  iconSide = "right",
  initCollapsed = false,
  margin,
  maxHeight,
  maxWidth,
  minHeight,
  minWidth,
  padding,
  scroll,
  width,
}: Readonly<IAccordionProps>): JSX.Element => {
  const [collapsed, setCollapsed] = useState(initCollapsed);
  const toggleCollapsed = useCallback((): void => {
    setCollapsed(!collapsed);
  }, [collapsed, setCollapsed]);

  return (
    <AccordionContainer>
      <AccordionHeader
        collapsed={collapsed}
        iconSide={iconSide}
        onClick={toggleCollapsed}
      >
        <IconWrapper>
          <FontAwesomeIcon icon={faAngleUp} />
        </IconWrapper>
        <p className={"f4"}>{header}</p>
      </AccordionHeader>
      <Container
        height={collapsed ? "0" : height}
        margin={margin}
        maxHeight={maxHeight}
        maxWidth={maxWidth}
        minHeight={minHeight}
        minWidth={minWidth}
        padding={collapsed ? "0" : padding}
        scroll={scroll}
        width={width}
      >
        {children}
      </Container>
    </AccordionContainer>
  );
};

export type { IAccordionProps };
export { Accordion };
