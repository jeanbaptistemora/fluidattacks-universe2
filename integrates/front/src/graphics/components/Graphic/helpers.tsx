/* eslint-disable react/no-multi-comp  -- Needed to declare various small helpers components */
import React from "react";

import { translate } from "utils/translations/translate";

interface IDaysLabelProps {
  days: string;
  isEqual: boolean;
}

const labels: Record<string, string> = {
  "30": translate.t("analytics.limitData.thirtyDays.text"),
  "90": translate.t("analytics.limitData.ninetyDays.text"),
  allTime: translate.t("analytics.limitData.all.text"),
};

const DaysLabel: React.FC<IDaysLabelProps> = ({
  days,
  isEqual,
}: IDaysLabelProps): JSX.Element => {
  const label = labels[days];

  return <div className={"pointer"}>{isEqual ? <b>{label}</b> : label}</div>;
};

interface IDocumentMergedProps {
  label: string;
  isEqual: boolean;
}

const DocumentMerged: React.FC<IDocumentMergedProps> = ({
  isEqual,
  label,
}: IDocumentMergedProps): JSX.Element => (
  <div className={"dark-red pointer"}>{isEqual ? <b>{label}</b> : label}</div>
);

export { DaysLabel, DocumentMerged };
