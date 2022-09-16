/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import {
  faBullhorn,
  faCheck,
  faQuestion,
  faUser,
} from "@fortawesome/free-solid-svg-icons";
import type { Meta, Story } from "@storybook/react";
import React from "react";

import { NavBar } from ".";
import { Button } from "components/Button";

const config: Meta = {
  component: NavBar,
  title: "components/NavBar",
};

const Default: Story = (): JSX.Element => (
  <NavBar>
    <Button icon={faBullhorn} size={"sm"}>
      {"News"}
    </Button>
    <Button icon={faCheck} size={"sm"}>
      {"To-do"}
    </Button>
    <Button icon={faQuestion} size={"sm"}>
      {"Help"}
    </Button>
    <Button icon={faUser} size={"sm"}>
      {"John"}
    </Button>
  </NavBar>
);

export { Default };
export default config;
