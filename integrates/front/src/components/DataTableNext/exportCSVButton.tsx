import { CSVExport } from "react-bootstrap-table2-toolkit";
import { FluidIcon } from "components/FluidIcon";
import React from "react";
import type { ToolkitProviderProps } from "react-bootstrap-table2-toolkit";
import { TooltipWrapper } from "components/TooltipWrapper";
import style from "components/DataTableNext/index.css";
import { translate } from "utils/translations/translate";

export const ExportCSVButtonWrapper: React.FC<ToolkitProviderProps> = (
  // Readonly utility type doesn't seem to work on ToolkitProviderProps
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: ToolkitProviderProps
): JSX.Element => {
  const { csvProps } = props;
  const { ExportCSVButton } = CSVExport;

  return (
    <TooltipWrapper message={translate.t("group.findings.exportCsv.tooltip")}>
      <div className={style.buttonWrapper}>
        <ExportCSVButton
          // This technique is used by react-bootstrap-table2 creators
          // eslint-disable-next-line react/jsx-props-no-spreading
          {...csvProps}
          // We need className to override default styles
          // eslint-disable-next-line react/forbid-component-props
          className={style.exportCsv}
        >
          <FluidIcon icon={"export"} />
          &nbsp;{translate.t("group.findings.exportCsv.text")}
        </ExportCSVButton>
      </div>
    </TooltipWrapper>
  );
};
