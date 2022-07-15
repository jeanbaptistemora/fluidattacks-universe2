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
import { Tooltip } from "components/Tooltip";

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
    <Tooltip id={"filterTooltip"} tip={t("table.tooltip")}>
      <Button onClick={handleUpdateEnableFilter}>
        <FontAwesomeIcon icon={isFilterEnabled ? faMinus : faPlus} />
        &nbsp;
        {t("table.filters")}
      </Button>
    </Tooltip>
  );
};
