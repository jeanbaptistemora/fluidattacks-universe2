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
      <p
        className={"f5 lh-title ma0 mid-gray pr1-l tr-l tl-m tl-ns ws-pre-wrap"}
      >
        {isEmpty ? t("searchFindings.tabVuln.notApplicable") : value}
      </p>
    </React.StrictMode>
  );
};
