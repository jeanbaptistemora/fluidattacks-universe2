import React from "react";

import { Container } from "../../../../components/Container";
import type { IContainerProps } from "../../../../components/Container/types";

const TextContainer: React.FC<IContainerProps> = ({
  children,
}): JSX.Element => (
  <Container center={true} maxWidth={"1200px"} ph={4} pv={5}>
    {children}
  </Container>
);

export { TextContainer };
