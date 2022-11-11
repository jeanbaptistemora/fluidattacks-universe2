/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";

import { TableLink } from "components/Table/styles";
import { Tooltip } from "components/Tooltip";

export function formatLinkHandler(
  link: string,
  text: string,
  showInfo?: boolean,
  tip?: string
): JSX.Element {
  const linkComponent = <TableLink to={link}>{_.capitalize(text)}</TableLink>;
  if (showInfo ?? false) {
    return (
      <div>
        {linkComponent}
        &nbsp;
        <Tooltip
          disp={"inline"}
          effect={"solid"}
          id={`${_.camelCase(text)}Tooltip`}
          place={"top"}
          tip={tip}
        >
          <sup>
            <FontAwesomeIcon color={"#5c5c70"} icon={faInfoCircle} />
          </sup>
        </Tooltip>
      </div>
    );
  }

  return linkComponent;
}
