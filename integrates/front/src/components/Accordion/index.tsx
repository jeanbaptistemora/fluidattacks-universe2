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
  pb,
  pl,
  pr,
  pt,
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
        pb={collapsed ? "0" : pb}
        pl={collapsed ? "0" : pl}
        pr={collapsed ? "0" : pr}
        pt={collapsed ? "0" : pt}
        scroll={scroll}
        width={width}
      >
        {collapsed ? undefined : children}
      </Container>
    </AccordionContainer>
  );
};

export type { IAccordionProps };
export { Accordion };
