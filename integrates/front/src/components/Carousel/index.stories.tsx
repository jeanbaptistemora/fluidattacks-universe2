/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ICarouselProps } from ".";
import { Carousel } from ".";

const config: Meta = {
  component: Carousel,
  title: "components/Carousel",
};

const Template: Story<ICarouselProps> = (props): JSX.Element => (
  <Carousel {...props} />
);

const Default = Template.bind({});
Default.args = {
  contents: [...Array(3).keys()].map(
    (el: number): JSX.Element => <p key={el}>{`Content ${el}`}</p>
  ),
  tabs: ["", "", ""],
};

export { Default };
export default config;
