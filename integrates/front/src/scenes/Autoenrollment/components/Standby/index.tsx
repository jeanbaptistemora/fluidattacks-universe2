import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { Button } from "components/Button";
import { Lottie } from "components/Icon";
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
        <Row justify={"end"}>
          <Col>
            <Button id={"close-standby"} onClick={onClose} size={"sm"}>
              <FontAwesomeIcon icon={faClose} />
            </Button>
          </Col>
        </Row>
        <div className={"flex justify-center"}>
          <Lottie animationData={scan} size={150} />
        </div>
        <Row justify={"center"}>
          <Col>{children}</Col>
        </Row>
      </Col>
    </Row>
  );
};

export { Standby };
