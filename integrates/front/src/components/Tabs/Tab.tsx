/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { TabLink } from "./styles";

import { Tooltip } from "components/Tooltip";

interface ITabProps {
  id: string;
  link: string;
  tooltip?: string;
}

const Tab: React.FC<ITabProps> = ({
  children,
  id,
  link,
  tooltip = "",
}: Readonly<React.PropsWithChildren<ITabProps>>): JSX.Element => {
  return (
    <li>
      <Tooltip id={`${id}Tooltip`} tip={tooltip}>
        <TabLink id={id} to={link}>
          {children}
        </TabLink>
      </Tooltip>
    </li>
  );
};

export { Tab };
