/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faClose } from "@fortawesome/free-solid-svg-icons";
import type { FC, ReactNode } from "react";
import React, { Fragment } from "react";

import { Button } from "components/Button";
import { Lottie } from "components/Icon";
import { Col, Row } from "components/Layout";
import scan from "resources/scan.json";

interface IStandbyProps {
  children: ReactNode;
  onClose?: () => void;
}

const Standby: FC<IStandbyProps> = (
  props: Readonly<IStandbyProps>
): JSX.Element => {
  const { children, onClose = (): void => undefined } = props;

  return (
    <Fragment>
      <Row justify={"end"}>
        <Col>
          <Button
            icon={faClose}
            id={"close-standby"}
            onClick={onClose}
            size={"sm"}
          />
        </Col>
      </Row>
      <div className={"flex justify-center"}>
        <Lottie animationData={scan} size={150} />
      </div>
      <Row justify={"center"}>
        <Col>{children}</Col>
      </Row>
    </Fragment>
  );
};

export { Standby };
