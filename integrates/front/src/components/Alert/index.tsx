/* eslint-disable react/require-default-props */
import type { IconDefinition } from "@fortawesome/fontawesome-common-types";
import {
  faCheckCircle,
  faCircleExclamation,
  faCircleInfo,
  faTriangleExclamation,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { Box } from "./Box";
import type { IBoxProps } from "./Box";

import { Col, Row } from "components/Layout";

interface IAlertProps extends IBoxProps {
  children: React.ReactNode;
  icon?: boolean;
}

interface IIcons {
  icon: IconDefinition;
}

const icons: Record<IAlertProps["variant"], IIcons> = {
  error: {
    icon: faCircleExclamation,
  },
  info: {
    icon: faCircleInfo,
  },
  success: {
    icon: faCheckCircle,
  },
  warning: {
    icon: faTriangleExclamation,
  },
};

const Alert: React.FC<IAlertProps> = ({
  children,
  icon = false,
  variant,
}: IAlertProps): JSX.Element | null => {
  return (
    <Box variant={variant}>
      <Row align={"center"}>
        {icon ? (
          <React.Fragment>
            <Col large={"10"} medium={"10"} small={"10"}>
              <FontAwesomeIcon icon={icons[variant].icon} />
            </Col>
            <Col large={"90"} medium={"90"} small={"90"}>
              {children}
            </Col>
          </React.Fragment>
        ) : (
          <Col>{children}</Col>
        )}
      </Row>
    </Box>
  );
};

export type { IAlertProps };
export { Alert };
