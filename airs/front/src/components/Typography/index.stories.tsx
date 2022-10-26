/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React from "react";

import type { ITextProps } from "./Text/types";

import { Text, Title } from ".";

const config: Meta = {
  component: Text,
  subcomponents: { Title },
  title: "components/Typography",
};

const TextTemplate: Story<PropsWithChildren<ITextProps>> = (
  props
): JSX.Element => <Text {...props} />;

const DefaultText = TextTemplate.bind({});
DefaultText.args = {
  children: "Example text",
  color: "#2e2e38",
};

const Header1: Story = (): JSX.Element => (
  <Title color={"#2e2e38"} level={1} size={"big"}>
    {"H1 Bold (700) 48px (3rem) | line-height: 56px"}
  </Title>
);

const Header2: Story = (): JSX.Element => (
  <Title color={"#2e2e38"} level={2} size={"medium"}>
    {"H2 Bold (700) 36px (2.25rem) | line-height: 48px"}
  </Title>
);

const Header3: Story = (): JSX.Element => (
  <Title color={"#2e2e38"} level={3} size={"small"}>
    {"H3 Semibold (600) 24px (1.5rem) | line-height: 40px"}
  </Title>
);

const Header4: Story = (): JSX.Element => (
  <Title color={"#2e2e38"} level={4} size={"xs"}>
    {"H4 Semibold (600) 20px (1.25rem) | line-height: 32px"}
  </Title>
);

export { DefaultText, Header1, Header2, Header3, Header4 };
export default config;
