import React from "react";

import { Container } from "../../../../components/Container";
import type { IContainerProps } from "../../../../components/Container/types";

const GridContainer: React.FC<IContainerProps> = ({
  children,
}): JSX.Element => (
  <Container
    center={true}
    direction={"row"}
    display={"flex"}
    justify={"center"}
    maxWidth={"1504px"}
    pb={5}
    ph={4}
    wrap={"wrap"}
  >
    {children}
  </Container>
);

export { GridContainer };
