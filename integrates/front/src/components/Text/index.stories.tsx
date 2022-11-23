/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React from "react";

import type { ITextProps } from ".";
import { Text } from ".";

const config: Meta = {
  component: Text,
  title: "components/Text",
};

const Template: Story<PropsWithChildren<ITextProps>> = (props): JSX.Element => (
  <Text {...props} />
);

const Default = Template.bind({});
Default.args = {
  bright: 5,
  children: "Example Text",
  hoverBright: 3,
  hoverTone: "red",
  ml: 5,
  size: "medium",
  tone: "dark",
};

const BigText: Story = (): JSX.Element => {
  return (
    <Text
      bright={5}
      hoverBright={3}
      hoverTone={"red"}
      ml={5}
      size={"big"}
      tone={"dark"}
    >
      {"Big heading"}
    </Text>
  );
};

const MediumText: Story = (): JSX.Element => {
  return (
    <Text
      bright={5}
      hoverBright={3}
      hoverTone={"red"}
      ml={5}
      mt={3}
      size={"medium"}
      tone={"dark"}
    >
      {"Medium heading"}
    </Text>
  );
};

const SmallText: Story = (): JSX.Element => {
  return (
    <Text
      bright={5}
      hoverBright={3}
      hoverTone={"red"}
      ml={5}
      mt={3}
      tone={"dark"}
    >
      {"Body text"}
    </Text>
  );
};

const XsText: Story = (): JSX.Element => {
  return (
    <Text
      bright={5}
      hoverBright={3}
      hoverTone={"red"}
      ml={5}
      mt={3}
      size={"xs"}
      tone={"dark"}
    >
      {"Body text"}
    </Text>
  );
};

export { Default, BigText, MediumText, SmallText, XsText };
export default config;
