/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import { faDesktop, faSkull } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { Meta, Story } from "@storybook/react";
import React from "react";

import {
  Indicator,
  IndicatorIcon,
  IndicatorTitle,
  IndicatorValue,
} from "./Indicator";

import { Indicators } from ".";

const config: Meta = {
  component: Indicators,
  title: "Components/Indicators",
};

const Template: Story = (): JSX.Element => (
  <Indicators>
    <Indicator>
      <IndicatorIcon>
        <FontAwesomeIcon icon={faDesktop} />
      </IndicatorIcon>
      <IndicatorTitle>{"Total types of vulnerabilities"}</IndicatorTitle>
      <IndicatorValue>{92}</IndicatorValue>
    </Indicator>
    <Indicator>
      <IndicatorIcon>
        <FontAwesomeIcon icon={faSkull} />
      </IndicatorIcon>
      <IndicatorTitle>{"Total vulnerabilities"}</IndicatorTitle>
      <IndicatorValue>{1570}</IndicatorValue>
    </Indicator>
  </Indicators>
);

const Default = Template.bind({});

export { Default };
export default config;
