import React from "react";

import { translate } from "utils/translations/translate";

interface IDaysLabelProps {
  days: string;
  isEqual: boolean;
}

const labels: Record<string, string> = {
  "30": translate.t("analytics.limitData.thirtyDays"),
  "90": translate.t("analytics.limitData.ninetyDays"),
  allTime: translate.t("analytics.limitData.all"),
};

export const DaysLabel: React.FC<IDaysLabelProps> = (
  props: IDaysLabelProps
): JSX.Element => {
  const { days, isEqual } = props;
  const label = labels[days];

  return <div>{isEqual ? <b>{label}</b> : label}</div>;
};
