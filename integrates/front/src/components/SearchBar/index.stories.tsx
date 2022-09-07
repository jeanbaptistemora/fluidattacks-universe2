/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ISearchBarProps } from ".";
import { SearchBar } from ".";

const config: Meta = {
  component: SearchBar,
  title: "components/SearchBar",
};

const Default: Story<ISearchBarProps> = (props): JSX.Element => (
  <SearchBar {...props} />
);

export { Default };
export default config;
