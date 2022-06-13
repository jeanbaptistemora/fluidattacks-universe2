import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import Lottie from "react-lottie-player";

import { ButtonOpacity } from "components/Button";
import { Col, Row } from "components/Layout";
import scan from "resources/scan.json";

interface IStandbyProps {
  children: React.ReactNode;
  onClose?: () => void;
}

const Standby: React.FC<IStandbyProps> = (
  props: Readonly<IStandbyProps>
): JSX.Element => {
  const { children, onClose = (): void => undefined } = props;

  return (
    <Row>
      <Col>
        <Row justify={"flex-end"}>
          <Col>
            <ButtonOpacity id={"close-standby"} onClick={onClose}>
              <FontAwesomeIcon icon={faClose} />
            </ButtonOpacity>
          </Col>
        </Row>
        <Row align={"center"} justify={"center"}>
          <Col>
            <Lottie
              animationData={scan}
              play={true}
              // eslint-disable-next-line react/forbid-component-props
              style={{ height: 150, margin: "auto", width: 150 }}
            />
          </Col>
        </Row>
        <Row justify={"center"}>
          <Col>{children}</Col>
        </Row>
      </Col>
    </Row>
  );
};

export { Standby };
