/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { Tab, Tabs } from ".";

const config: Meta = {
  subcomponents: { Tab, Tabs },
  title: "components/Tabs",
};

const Default: Story = (): JSX.Element => (
  <MemoryRouter initialEntries={["/vulns"]}>
    <Tabs>
      <Tab id={"test"} link={"/vulns"}>
        {"Vulnerabilities"}
      </Tab>
      <Tab id={"test"} link={"/analytics"}>
        {"Analytics"}
      </Tab>
    </Tabs>
  </MemoryRouter>
);

const WithTooltips: Story = (): JSX.Element => (
  <MemoryRouter initialEntries={["/vulns"]}>
    <Tabs>
      <Tab id={"test"} link={"/vulns"} tooltip={"View all reported vulns"}>
        {"Vulnerabilities"}
      </Tab>
      <Tab id={"test"} link={"/analytics"} tooltip={"Summary of the group"}>
        {"Analytics"}
      </Tab>
    </Tabs>
  </MemoryRouter>
);

export { Default, WithTooltips };
export default config;
