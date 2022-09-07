/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faAngleDown, faAngleUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type {
  ExpandColumnRendererProps,
  ExpandHeaderColumnRenderer,
} from "react-bootstrap-table-next";

const renderExpandIcon = ({
  expanded,
}: ExpandColumnRendererProps): JSX.Element =>
  expanded ? (
    <FontAwesomeIcon icon={faAngleUp} />
  ) : (
    <FontAwesomeIcon icon={faAngleDown} />
  );

const renderHeaderExpandIcon = ({
  isAnyExpands,
}: ExpandHeaderColumnRenderer): JSX.Element =>
  isAnyExpands ? (
    <FontAwesomeIcon icon={faAngleUp} />
  ) : (
    <FontAwesomeIcon icon={faAngleDown} />
  );

export { renderExpandIcon, renderHeaderExpandIcon };
