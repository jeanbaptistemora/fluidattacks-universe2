/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IDropdownProps } from ".";
import { Dropdown } from ".";
import { ButtonOpacity } from "components/Button";

const config: Meta = {
  component: Dropdown,
  title: "components/Dropdown",
};

const Template: Story<IDropdownProps> = (props): JSX.Element => (
  <div className={"vh-50 pl5"}>
    <Dropdown {...props} />
  </div>
);

const Default = Template.bind({});
Default.args = {
  align: "center",
  button: <ButtonOpacity>{"ShowOnHover"}</ButtonOpacity>,
  children: (
    <React.Fragment>
      {Array.from(Array(4).keys()).map(
        (el): JSX.Element => (
          <p className={"mv2"} key={el}>{`A very large option ${el}`}</p>
        )
      )}
    </React.Fragment>
  ),
};

export { Default };
export default config;
