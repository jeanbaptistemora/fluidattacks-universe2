import { faDownload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";
import type { ToolkitContextType } from "react-bootstrap-table2-toolkit";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";

export const ExportCSVButtonWrapper: React.FC<ToolkitContextType> = ({
  csvProps,
}: ToolkitContextType): JSX.Element => {
  const { t } = useTranslation();

  const handleClick = useCallback((): void => {
    csvProps.onExport();
  }, [csvProps]);

  return (
    <div>
      <TooltipWrapper
        id={"exportCsvTooltip"}
        message={t("group.findings.exportCsv.tooltip")}
      >
        <Button onClick={handleClick} variant={"secondary"}>
          <FontAwesomeIcon icon={faDownload} />
          &nbsp;{t("group.findings.exportCsv.text")}
        </Button>
      </TooltipWrapper>
    </div>
  );
};
