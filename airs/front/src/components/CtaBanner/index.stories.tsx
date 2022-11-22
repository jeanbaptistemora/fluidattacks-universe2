/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ICtaBannerProps } from "./types";

import { CtaBanner } from ".";

const config: Meta = {
  component: CtaBanner,
  title: "components/CtaBanner",
};

const Template: Story<React.PropsWithChildren<ICtaBannerProps>> = (
  props
): JSX.Element => <CtaBanner {...props} />;

const Default = Template.bind({});
Default.args = {
  button1Link: "/test/",
  button1Text: "Go to test",
  button2Link: "/other-test/",
  button2Text: "Go to other test",
  image: "airs/solutions/Index/application-security-solutions",
  paragraph:
    "This is a test paragraph that should show the behavior of the CTA",
  size: "big",
  sizeMd: "medium",
  sizeSm: "small",
  title: "This is a test title",
};

const JustText: Story = (): JSX.Element => (
  <CtaBanner
    button1Link={"/test/"}
    button1Text={"Go to test"}
    button2Link={"/other-test/"}
    button2Text={"Go to other test"}
    matomoAction={"Example"}
    paragraph={
      "This is a test paragraph that should show the behavior of the CTA"
    }
    size={"big"}
    sizeSm={"medium"}
    title={`This is a test title`}
  />
);

export { Default, JustText };
export default config;
