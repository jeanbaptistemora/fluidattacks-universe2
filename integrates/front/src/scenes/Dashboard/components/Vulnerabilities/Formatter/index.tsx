/* eslint-disable react/forbid-component-props
  --------
  Need it to override default background color based on condition
*/
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Badge } from "components/Badge";
import { getBgColor } from "utils/colors";

interface IStatus {
  status: string;
}

const Status: React.FC<IStatus> = ({ status }: IStatus): JSX.Element => {
  const { t } = useTranslation();
  const formatedStatus: string =
    _.upperCase(status) === "OK" ? _.upperCase(status) : _.capitalize(status);
  const currentStateBgColor = getBgColor(_.capitalize(status));

  return (
    <Badge variant={currentStateBgColor}>
      {formatedStatus === "On_hold"
        ? t("searchFindings.tabVuln.onHold")
        : formatedStatus.split(" ")[0]}
    </Badge>
  );
};

const statusFormatter = (value: string): JSX.Element => (
  <Status status={value} />
);

export { statusFormatter, Status };
