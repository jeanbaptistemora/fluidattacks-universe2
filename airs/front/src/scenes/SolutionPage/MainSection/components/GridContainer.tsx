import React from "react";

import { Container } from "../../../../components/Container";
import type { IContainerProps } from "../../../../components/Container/types";
import { Grid } from "../../../../components/Grid";

const GridContainer: React.FC<IContainerProps> = ({
  children,
}): JSX.Element => (
  <Container center={true} maxWidth={"1440px"} pb={5} ph={4}>
    <Grid columns={3} columnsMd={2} columnsSm={1} gap={"1rem"}>
      {children}
    </Grid>
  </Container>
);

export { GridContainer };
