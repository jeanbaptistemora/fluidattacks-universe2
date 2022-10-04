/* eslint-disable @typescript-eslint/no-magic-numbers */
/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC, ReactNode } from "react";
import React from "react";

import { Dropdown } from "components/Dropdown";
import { Text } from "components/Text";

type TSize = "big" | "medium" | "small";

interface IInfoDropdownProps {
  alignDropdown?: "center" | "left" | "right";
  size?: TSize;
  sup?: boolean;
  children?: ReactNode | string;
}

const InfoDropdown: FC<IInfoDropdownProps> = ({
  alignDropdown = "left",
  size = "small",
  sup = true,
  children,
}: Readonly<IInfoDropdownProps>): JSX.Element => (
  <Dropdown
    align={alignDropdown}
    button={
      sup ? (
        <sup>
          <Text size={size}>
            <FontAwesomeIcon icon={faInfoCircle} />
          </Text>
        </sup>
      ) : (
        <Text size={size}>
          <FontAwesomeIcon icon={faInfoCircle} />
        </Text>
      )
    }
    minWidth={"150px"}
  >
    {children}
  </Dropdown>
);

export type { IInfoDropdownProps };
export { InfoDropdown };
