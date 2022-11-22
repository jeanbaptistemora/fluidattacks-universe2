/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { CompleteStatus } from "./completeStatus";

import { Tag } from "components/Tag";
import { getBgColor } from "utils/colors";

interface IStatus {
  status: string | undefined;
}

const Status: React.FC<IStatus> = ({ status }: IStatus): JSX.Element => {
  const { t } = useTranslation();
  const formatedStatus: string = _.capitalize(status);
  const currentStateBgColor = getBgColor(_.capitalize(status));

  return (
    <Tag variant={currentStateBgColor}>
      {formatedStatus === "On_hold"
        ? t("searchFindings.tabVuln.onHold")
        : formatedStatus.split(" ")[0]}
    </Tag>
  );
};

const statusFormatter = (
  value: string | undefined,
  completeStatus?: boolean
): JSX.Element => {
  return !_.isUndefined(completeStatus) && completeStatus ? (
    <CompleteStatus status={value} />
  ) : (
    <Status status={value} />
  );
};

export type { IStatus };
export { statusFormatter, Status };
