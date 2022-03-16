import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

export const Value: React.FC<{ value: number | string | undefined }> = ({
  value,
}: {
  value: number | string | undefined;
}): JSX.Element => {
  const { t } = useTranslation();
  const isEmpty: boolean = _.isNumber(value)
    ? value === 0
    : _.isEmpty(value) || value === "-";

  return (
    <React.StrictMode>
      <span
        className={"f5 lh-title ma0 pr1-l ws-pre-wrap"}
        style={{ color: "#8f8fa3" }}
      >
        {isEmpty ? t("searchFindings.tabVuln.notApplicable") : value}
      </span>
    </React.StrictMode>
  );
};
