/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  --------
  We need className to override default styles from react-bootstrap and props
  spreading is the technique used by react-bootstrap-table2 creators to pass
  down props
  */
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";

interface IFilterButtonProps {
  isFilterEnabled: boolean;
  onUpdateEnableFilter: () => void;
}

export const FiltersButton: React.FC<IFilterButtonProps> = (
  props: Readonly<IFilterButtonProps>
): JSX.Element => {
  const { onUpdateEnableFilter, isFilterEnabled } = props;
  const { t } = useTranslation();

  function handleUpdateEnableFilter(): void {
    if (!_.isUndefined(onUpdateEnableFilter)) {
      onUpdateEnableFilter();
    }
  }

  return (
    <TooltipWrapper id={"filterTooltip"} message={t("dataTableNext.tooltip")}>
      <Button onClick={handleUpdateEnableFilter} variant={"secondary"}>
        {isFilterEnabled ? (
          <FontAwesomeIcon icon={faMinus} />
        ) : (
          <FontAwesomeIcon icon={faPlus} />
        )}
        &nbsp;
        {t("dataTableNext.filters")}
      </Button>
    </TooltipWrapper>
  );
};
