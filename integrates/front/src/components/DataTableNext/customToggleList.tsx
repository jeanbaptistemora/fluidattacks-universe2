/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import { faCog } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useState } from "react";
import type { ColumnDescription } from "react-bootstrap-table-next";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import type { ICustomToggleProps } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  Row,
  RowCenter,
} from "styles/styledComponents";

export const CustomToggleList: React.FC<ICustomToggleProps> = (
  props: Readonly<ICustomToggleProps>
): JSX.Element => {
  const { t } = useTranslation();
  const {
    propsTable: { onColumnToggle: sideEffects },
    propsToggle: { columns, toggles, onColumnToggle },
  } = props;
  const [hidden, setHidden] = useState(false);
  function handleOpenTableSetClick(): void {
    setHidden(true);
  }
  function handleCloseTableSetClick(): void {
    setHidden(false);
  }

  return (
    <div>
      <TooltipWrapper
        id={"toogleToolTip"}
        message={t("group.findings.tableSet.btn.tooltip")}
      >
        <Button onClick={handleOpenTableSetClick}>
          <FontAwesomeIcon icon={faCog} />
          &nbsp;
          {t("group.findings.tableSet.btn.text")}
        </Button>
      </TooltipWrapper>
      <Modal
        headerTitle={t("group.findings.tableSet.modalTitle")}
        onEsc={handleCloseTableSetClick}
        open={hidden}
      >
        <RowCenter>
          <div
            className={"btn-group btn-group-toggle btn-group-vertical"}
            data-toggle={"buttons"}
          >
            {columns
              .map(
                (
                  column: ColumnDescription
                ): ColumnDescription & {
                  toggle: boolean;
                } => ({
                  ...column,
                  toggle: toggles[column.dataField as number],
                })
              )
              .map((column): JSX.Element => {
                function handleClick(): void {
                  onColumnToggle(column.dataField as string);

                  if (!_.isUndefined(sideEffects)) {
                    sideEffects(column.dataField as string);
                  }
                }

                return (
                  <Row key={column.dataField}>
                    <input
                      checked={column.toggle}
                      name={column.dataField}
                      onChange={handleClick}
                      type={"checkbox"}
                    />
                    <ControlLabel className={"ml1"}>{column.text}</ControlLabel>
                  </Row>
                );
              })}
          </div>
        </RowCenter>
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={handleCloseTableSetClick}>
                {t("group.findings.report.modalClose")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
    </div>
  );
};
