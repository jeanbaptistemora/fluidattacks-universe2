/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faCog } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { RowData } from "@tanstack/react-table";
import type { ReactElement } from "react";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { ToggleContainer } from "./styles";
import type { IToggleProps } from "./types";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { Modal } from "components/Modal";
import { Switch } from "components/Switch";

export const ToggleFunction = <TData extends RowData>(
  props: IToggleProps<TData>
): JSX.Element => {
  const { table } = props;
  const { t } = useTranslation();
  const [hidden, setHidden] = useState(true);
  function showModal(): void {
    setHidden(false);
  }
  function hideModal(): void {
    setHidden(true);
  }

  return (
    <div id={"columns-filter"}>
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
        <ToggleContainer id={"columns-buttons"}>
          {table.getAllLeafColumns().map((column): ReactElement => {
            return (
              <Row align={"center"} key={column.id}>
                <Col lg={70} md={70} sm={70}>
                  {column.columnDef.header}
                </Col>
                <Col lg={30} md={30} sm={30}>
                  <Switch
                    checked={column.getIsVisible()}
                    name={column.id}
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
