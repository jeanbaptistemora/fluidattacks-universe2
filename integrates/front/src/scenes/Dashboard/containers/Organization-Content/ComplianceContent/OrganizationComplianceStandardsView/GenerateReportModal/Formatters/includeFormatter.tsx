import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IUnfulfilledStandardData } from "../types";
import { Switch } from "components/Switch";

interface IIncludeFormatterProps {
  row: IUnfulfilledStandardData;
  changeFunction: (row: IUnfulfilledStandardData) => void;
}

const IncludeFormatter: React.FC<IIncludeFormatterProps> = ({
  row,
  changeFunction,
}: IIncludeFormatterProps): JSX.Element => {
  const { t } = useTranslation();
  const handleOnChange: () => void = useCallback((): void => {
    changeFunction(row);
  }, [changeFunction, row]);

  return (
    <Switch
      checked={row.include}
      label={{
        off: t(
          "organization.tabs.compliance.tabs.standards.generateReportModal.exclude"
        ),
        on: t(
          "organization.tabs.compliance.tabs.standards.generateReportModal.include"
        ),
      }}
      onChange={handleOnChange}
    />
  );
};

export const includeFormatter = (
  row: IUnfulfilledStandardData,
  changeFunction: (row: IUnfulfilledStandardData) => void
): JSX.Element => (
  <IncludeFormatter changeFunction={changeFunction} row={row} />
);
