/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import { useArgs } from "@storybook/addons";
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React, { useCallback } from "react";

import type { ISidePanelProps } from ".";
import { SidePanel } from ".";
import { Button } from "components/Button";

const config: Meta = {
  component: SidePanel,
  title: "components/SidePanel",
};

const Template: Story<PropsWithChildren<ISidePanelProps>> = (
  props
): JSX.Element => {
  const [, setArgs] = useArgs();
  const openPanel = useCallback((): void => {
    setArgs({ open: true });
  }, [setArgs]);
  const closePanel = useCallback((): void => {
    setArgs({ open: false });
  }, [setArgs]);

  return (
    <React.Fragment>
      <Button onClick={openPanel} variant={"primary"}>
        {"Open panel"}
      </Button>
      <SidePanel {...props} onClose={closePanel}>
        <p>{"Panel body goes here"}</p>
      </SidePanel>
    </React.Fragment>
  );
};

const Default = Template.bind({});
Default.args = {
  open: false,
};

export { Default };
export default config;
