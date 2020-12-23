import { Button } from "components/Button";
import type { Column } from "react-bootstrap-table-next";
import type { ColumnToggle } from "react-bootstrap-table2-toolkit";
import { Glyphicon } from "react-bootstrap";
import type { ICustomToggleProps } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import { useTranslation } from "react-i18next";
import {
  ButtonToolbar,
  ControlLabel,
  Row,
  RowCenter,
} from "styles/styledComponents";

export const CustomToggleList: React.FC<ICustomToggleProps> = (
  // Readonly utility type doesn't work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<ICustomToggleProps>
): JSX.Element => {
  const { t } = useTranslation();
  const {
    propsTable: { onColumnToggle: sideEffects },
    propsToggle: { columns, toggles, onColumnToggle },
  } = props;
  const [hidden, setHidden] = React.useState(false);
  function handleOpenTableSetClick(): void {
    setHidden(true);
  }
  function handleCloseTableSetClick(): void {
    setHidden(false);
  }

  return (
    <div>
      <TooltipWrapper message={t("group.findings.tableSet.btn.tooltip")}>
        <Button onClick={handleOpenTableSetClick}>
          <Glyphicon glyph={"glyphicon glyphicon-cog"} />
          &nbsp;
          {t("group.findings.tableSet.btn.text")}
        </Button>
      </TooltipWrapper>
      <Modal
        headerTitle={t("group.findings.tableSet.modal_title")}
        open={hidden}
      >
        <RowCenter>
          <div
            className={"btn-group btn-group-toggle btn-group-vertical"}
            data-toggle={"buttons"}
          >
            {columns
              .map((column: Readonly<Column>): Column & {
                toggle: boolean;
              } => ({
                ...column,
                toggle: toggles[column.dataField],
              }))
              .map(
                (column: Readonly<ColumnToggle>): JSX.Element => {
                  function handleClick(): void {
                    onColumnToggle(column.dataField);

                    if (!_.isUndefined(sideEffects)) {
                      sideEffects(column.dataField);
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
                      <ControlLabel>{column.text}</ControlLabel>
                    </Row>
                  );
                }
              )}
          </div>
        </RowCenter>
        <ButtonToolbar>
          <Button onClick={handleCloseTableSetClick}>
            {t("group.findings.report.modal_close")}
          </Button>
        </ButtonToolbar>
      </Modal>
    </div>
  );
};
