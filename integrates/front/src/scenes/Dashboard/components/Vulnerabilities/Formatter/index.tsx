import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Badge } from "components/Badge";
import { getBgColor } from "utils/colors";

interface IStatus {
  status: string | undefined;
}

const Status: React.FC<IStatus> = ({ status }: IStatus): JSX.Element => {
  const { t } = useTranslation();
  const formatedStatus: string = ["OK", "N/A"].includes(
    status ?? "".toUpperCase()
  )
    ? status ?? "".toUpperCase()
    : _.capitalize(status);
  const currentStateBgColor = getBgColor(_.capitalize(status));

  return (
    <Badge variant={currentStateBgColor}>
      {formatedStatus === "On_hold"
        ? t("searchFindings.tabVuln.onHold")
        : formatedStatus.split(" ")[0]}
    </Badge>
  );
};

const statusFormatter = (value: string | undefined): JSX.Element => (
  <Status status={value} />
);

export { statusFormatter, Status };
