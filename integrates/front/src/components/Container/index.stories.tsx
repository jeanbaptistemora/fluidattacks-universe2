/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IContainerProps } from ".";
import { Container } from ".";

const config: Meta = {
  component: Container,
  title: "components/Container",
};

const Template: Story<React.PropsWithChildren<IContainerProps>> = (
  props
): JSX.Element => <Container {...props} />;

const Default = Template.bind({});
Default.args = {
  children: (
    <div className={"flex flex-wrap justify between"}>
      {[...Array(15).keys()].map(
        (el): JSX.Element => (
          <p className={"mv5 w-25 tc"} key={el}>{`Content ${el}`}</p>
        )
      )}
    </div>
  ),
  height: "300px",
};

export { Default };
export default config;
