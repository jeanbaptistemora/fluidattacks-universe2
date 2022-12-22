import React from "react";

import { Container } from "../../../../components/Container";
import { Text } from "../../../../components/Typography";
import type { ITextProps } from "../../../../components/Typography";

const Paragraph: React.FC<ITextProps> = ({ children }): JSX.Element => (
  <Container mv={3}>
    <Text color={"#535365"}>{children}</Text>
  </Container>
);

export { Paragraph };
