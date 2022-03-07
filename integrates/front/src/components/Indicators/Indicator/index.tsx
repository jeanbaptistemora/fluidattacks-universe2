import type { IconProp } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { PropsWithChildren } from "react";
import React from "react";

import { Container, Icon, Title, Value } from "./styles";

interface IIndicatorProps {
  title: string;
  icon: IconProp;
}

const Indicator = ({
  children,
  icon,
  title,
}: PropsWithChildren<IIndicatorProps>): JSX.Element => {
  return (
    <Container>
      <Icon>
        <FontAwesomeIcon icon={icon} />
      </Icon>
      <Title>{title}</Title>
      <Value>{children}</Value>
    </Container>
  );
};

export { Indicator };
