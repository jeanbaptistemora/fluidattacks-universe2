import React from "react";

import { Container } from "../../../../components/Container";
import { Title } from "../../../../components/Typography";
import type { ITitleProps } from "../../../../components/Typography";

const Header2: React.FC<ITitleProps> = ({ children }): JSX.Element => (
  <Container pv={3}>
    <Title color={"#2e2e38"} level={2} size={"small"}>
      {children}
    </Title>
  </Container>
);

export { Header2 };
