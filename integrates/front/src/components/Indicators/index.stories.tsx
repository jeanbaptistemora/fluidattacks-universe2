/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import { faDesktop, faSkull } from "@fortawesome/free-solid-svg-icons";
import type { Meta, Story } from "@storybook/react";
import React from "react";

import { Indicator } from "./Indicator";

import { Indicators } from ".";

const config: Meta = {
  component: Indicators,
  title: "components/Indicators",
};

const Default: Story = (): JSX.Element => (
  <Indicators>
    <Indicator icon={faDesktop} title={"Total types of vulnerabilities"}>
      {"92"}
    </Indicator>
    <Indicator icon={faSkull} title={"Total vulnerabilities"}>
      {"1570"}
    </Indicator>
  </Indicators>
);

export { Default };
export default config;
