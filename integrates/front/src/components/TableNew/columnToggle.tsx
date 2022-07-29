import { faCog } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ReactElement } from "react";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { ToggleContainer } from "./styles";
import type { IToggleProps } from "./types";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { Modal } from "components/Modal";
import { Switch } from "components/Switch";

export const ToggleFunction = <TData extends object>(
  props: IToggleProps<TData>
): JSX.Element => {
  const { id, table } = props;
  const { t } = useTranslation();
  const [hidden, setHidden] = useState(true);
  function showModal(): void {
    setHidden(false);
  }
  function hideModal(): void {
    setHidden(true);
  }

  return (
    <div id={id}>
      <Button onClick={showModal}>
        <FontAwesomeIcon icon={faCog} />
        &nbsp;
        {t("group.findings.tableSet.btn.text")}
      </Button>
      <Modal
        onClose={hideModal}
        open={!hidden}
        title={t("group.findings.tableSet.modalTitle")}
      >
        <ToggleContainer>
          {table.getAllLeafColumns().map((column): ReactElement => {
            return (
              <Row align={"center"} key={column.id}>
                <Col large={"70"} medium={"70"} small={"70"}>
                  {column.columnDef.header}
                </Col>
                <Col large={"30"} medium={"30"} small={"30"}>
                  <Switch
                    checked={column.getIsVisible()}
                    onChange={column.getToggleVisibilityHandler()}
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
