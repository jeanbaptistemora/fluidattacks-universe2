import { Button } from "../Button";
import { Column } from "react-bootstrap-table-next";
import { ColumnToggle } from "react-bootstrap-table2-toolkit";
import { ICustomToggleProps } from "./types";
import { Modal } from "../Modal";
import React from "react";
import { TooltipWrapper } from "../TooltipWrapper";
import _ from "lodash";
import translate from "../../utils/translations/translate";
import { ButtonToolbar, Checkbox, Col, Glyphicon } from "react-bootstrap";

export const CustomToggleList: React.FC<ICustomToggleProps> = (
  // Readonly utility type doesn't work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<ICustomToggleProps>
): JSX.Element => {
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
      <TooltipWrapper
        message={translate.t("group.findings.tableSet.btn.tooltip")}
      >
        <Button onClick={handleOpenTableSetClick}>
          <Glyphicon glyph={"glyphicon glyphicon-cog"} />
          &nbsp;
          {translate.t("group.findings.tableSet.btn.text")}
        </Button>
      </TooltipWrapper>
      <Modal
        footer={
          // We need className to override default styles from react-bootstrap
          // eslint-disable-next-line react/forbid-component-props
          <ButtonToolbar className={"pull-right"}>
            <Button onClick={handleCloseTableSetClick}>
              {translate.t("group.findings.report.modal_close")}
            </Button>
          </ButtonToolbar>
        }
        headerTitle={translate.t("group.findings.tableSet.modal_title")}
        open={hidden}
      >
        <Col mdOffset={5}>
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
                    <Checkbox
                      checked={column.toggle}
                      key={column.dataField}
                      name={column.dataField}
                      onChange={handleClick}
                    >
                      {column.text}
                    </Checkbox>
                  );
                }
              )}
          </div>
        </Col>
      </Modal>
    </div>
  );
};
