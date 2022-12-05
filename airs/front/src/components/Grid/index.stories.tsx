/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IGridProps } from "./types";

import { Grid } from ".";
import { Container } from "../Container";

const config: Meta = {
  component: Grid,
  title: "components/Grid",
};

const Template: Story<React.PropsWithChildren<IGridProps>> = (
  props
): JSX.Element => (
  <Grid {...props}>
    {[...Array(10).keys()].map(
      (el): JSX.Element => (
        <Container
          bgColor={"#f4f4f6"}
          key={el}
          ph={5}
          pv={5}
        >{`Content ${el}`}</Container>
      )
    )}
  </Grid>
);

const Default = Template.bind({});
Default.args = {
  columns: 3,
  columnsMd: 2,
  columnsSm: 1,
  gap: "1rem",
};

export { Default };
export default config;
