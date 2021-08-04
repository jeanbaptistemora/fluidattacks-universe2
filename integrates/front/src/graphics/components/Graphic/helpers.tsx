/* eslint-disable react/no-multi-comp  -- Needed to declare various small helpers components */
import React from "react";

import { TooltipWrapper } from "components/TooltipWrapper";
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

const DaysLabel: React.FC<IDaysLabelProps> = (
  props: IDaysLabelProps
): JSX.Element => {
  const { days, isEqual } = props;
  const label = labels[days];

  return <div className={"pointer"}>{isEqual ? <b>{label}</b> : label}</div>;
};

interface IDocumentMergedProps {
  label: string;
  isEqual: boolean;
  tooltip: string;
}

const DocumentMerged: React.FC<IDocumentMergedProps> = ({
  isEqual,
  label,
  tooltip,
}: IDocumentMergedProps): JSX.Element => (
  <TooltipWrapper id={tooltip.split(" ").join("_")} message={tooltip}>
    <div className={"dark-red pointer"}>{isEqual ? <b>{label}</b> : label}</div>
  </TooltipWrapper>
);

export { DaysLabel, DocumentMerged };
