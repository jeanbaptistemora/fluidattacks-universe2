import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Tag } from "components/Tag";
import { getBgColor } from "utils/colors";

interface IStatus {
  value: string | undefined;
}

const VulnTag: React.FC<IStatus> = ({ value }: IStatus): JSX.Element => {
  const { t } = useTranslation();
  const formatedStatus: string = _.capitalize(value);
  const currentStateBgColor = getBgColor(_.capitalize(value));

  return (
    <Tag variant={currentStateBgColor}>
      {formatedStatus === "On_hold"
        ? t("searchFindings.tabVuln.onHold")
        : formatedStatus.split(" ")[0]}
    </Tag>
  );
};

export type { IStatus };
export { VulnTag };
