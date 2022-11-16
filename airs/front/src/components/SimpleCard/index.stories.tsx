/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ISimpleCardProps } from "./types";

import { SimpleCard } from ".";

const config: Meta = {
  component: SimpleCard,
  title: "components/SimpleCard",
};

const Template: Story<React.PropsWithChildren<ISimpleCardProps>> = (
  props
): JSX.Element => <SimpleCard {...props} />;

const Default = Template.bind({});
Default.args = {
  bgColor: "#f4f4f6",
  description:
    "Our security testing, integrating DevSecOps techniques " +
    "such as SAST, DAST and SCA, supports your whole " +
    "software development process while ensuring smooth " +
    "communication between our red team and your developers.",
  descriptionColor: "#535365",
  image: "airs/solutions/devsecops/icon1",
  title: "Optimal integration of security testing",
  titleColor: "#2e2e38",
  width: "450px",
};

const JustDescription: Story = (): JSX.Element => (
  <SimpleCard
    bgColor={"#f4f4f6"}
    description={
      "Our security testing, integrating DevSecOps techniques " +
      "such as SAST, DAST and SCA, supports your whole " +
      "software development process while ensuring smooth " +
      "communication between our red team and your developers."
    }
    descriptionColor={"#535365"}
    image={"airs/solutions/devsecops/icon1"}
    width={"450px"}
  />
);

export { Default, JustDescription };
export default config;
