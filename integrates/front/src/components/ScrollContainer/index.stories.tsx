/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import { ScrollContainer } from ".";

const config: Meta = {
  component: ScrollContainer,
  title: "components/ScrollContainer",
};

const Template: Story = (props): JSX.Element => (
  <div className={"vh-50"}>
    <ScrollContainer {...props} />
  </div>
);

const Default = Template.bind({});
Default.args = {
  children: (
    <div>
      {Array.from(Array(10).keys()).map(
        (el): JSX.Element => (
          <p className={"mv4"} key={el}>{`Content ${el}`}</p>
        )
      )}
    </div>
  ),
};

export { Default };
export default config;
