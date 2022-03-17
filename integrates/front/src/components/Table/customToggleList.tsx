import { faCog } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { ToggleContainer, ToggleLabel } from "./styles";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { Modal } from "components/Modal";
import type { ICustomToggleProps } from "components/Table/types";
import { TooltipWrapper } from "components/TooltipWrapper";

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
        <Button
          id={"columns-filter"}
          onClick={handleOpenTableSetClick}
          variant={"secondary"}
        >
          <FontAwesomeIcon icon={faCog} />
          &nbsp;
          {t("group.findings.tableSet.btn.text")}
        </Button>
      </TooltipWrapper>
      <Modal
        onClose={handleCloseTableSetClick}
        open={hidden}
        size={"small"}
        title={t("group.findings.tableSet.modalTitle")}
      >
        <ToggleContainer id={"columns-buttons"}>
          {columns.map((column): JSX.Element => {
            function handleClick(): void {
              onColumnToggle(column.dataField as string);

              if (!_.isUndefined(sideEffects)) {
                sideEffects(column.dataField as string);
              }
            }

            return (
              <Row key={column.dataField}>
                <Col>
                  <ToggleLabel>{column.text}</ToggleLabel>
                </Col>
                <Col large={"25"} medium={"25"} small={"25"}>
                  <input
                    aria-label={column.dataField}
                    checked={toggles[column.dataField as number]}
                    name={column.dataField}
                    onChange={handleClick}
                    type={"checkbox"}
                  />
                </Col>
              </Row>
            );
          })}
        </ToggleContainer>
      </Modal>
    </div>
  );
};
