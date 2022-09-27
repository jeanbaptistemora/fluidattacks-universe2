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

type Nums1To7 = 1 | 2 | 3 | 4 | 5 | 6 | 7;

interface IInfoDropdownProps {
  alignDropdown: "center" | "left" | "right";
  size: Nums1To7;
  sup: boolean;
  children?: ReactNode;
}

const InfoDropdown: FC<IInfoDropdownProps> = ({
  alignDropdown = "left",
  size = 1,
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
    minWidth={"100px"}
  >
    {children}
  </Dropdown>
);

export type { IInfoDropdownProps };
export { InfoDropdown };
