/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC } from "react";
import React from "react";

import { Button } from "components/Button";

interface ICloseToastProps {
  closeToast: false | (() => void);
}

const CloseToast: FC<ICloseToastProps> = ({
  closeToast,
}: ICloseToastProps): JSX.Element => (
  <Button onClick={closeToast === false ? undefined : closeToast} size={"xs"}>
    <FontAwesomeIcon icon={faXmark} />
  </Button>
);

export type { ICloseToastProps };
export { CloseToast };
