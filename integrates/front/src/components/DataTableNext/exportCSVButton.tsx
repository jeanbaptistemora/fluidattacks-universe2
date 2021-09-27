import { faDownload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { ToolkitContextType } from "react-bootstrap-table2-toolkit";
import { CSVExport } from "react-bootstrap-table2-toolkit";
import { useTranslation } from "react-i18next";

import style from "components/DataTableNext/index.css";
import { TooltipWrapper } from "components/TooltipWrapper";

export const ExportCSVButtonWrapper: React.FC<ToolkitContextType> = (
  props: ToolkitContextType
): JSX.Element => {
  const { csvProps } = props;
  const { ExportCSVButton } = CSVExport;
  const { t } = useTranslation();

  return (
    <div>
      <TooltipWrapper
        id={"exportCsvTooltip"}
        message={t("group.findings.exportCsv.tooltip")}
      >
        <ExportCSVButton
          // This technique is used by react-bootstrap-table2 creators
          // eslint-disable-next-line react/jsx-props-no-spreading
          {...csvProps}
          // We need className to override default styles
          // eslint-disable-next-line react/forbid-component-props
          className={`${style.exportCsv} b--orgred ba btn-pa bg-bh bg-btn fw100 montserrat orgred svg-box`}
        >
          <FontAwesomeIcon icon={faDownload} />
          &nbsp;{t("group.findings.exportCsv.text")}
        </ExportCSVButton>
      </TooltipWrapper>
    </div>
  );
};
