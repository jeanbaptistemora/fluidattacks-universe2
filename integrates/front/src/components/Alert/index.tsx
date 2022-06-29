/* eslint-disable react/require-default-props */
import type { IconDefinition } from "@fortawesome/fontawesome-common-types";
import {
  faCheckCircle,
  faCircleExclamation,
  faCircleInfo,
  faTriangleExclamation,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect, useState } from "react";

import type { IAlertBoxProps } from "./Box";
import { AlertBox } from "./Box";

interface IAlertProps extends IAlertBoxProps {
  children: React.ReactNode;
  icon?: boolean;
  timer?: React.Dispatch<React.SetStateAction<boolean>>;
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
  timer = (): void => undefined,
  variant,
}: IAlertProps): JSX.Element | null => {
  const [seconds, setSeconds] = useState(0);
  useEffect((): VoidFunction => {
    const interval = setInterval((): void => {
      setSeconds((secs): number => secs + 1);
    }, 1000);

    return (): void => {
      clearInterval(interval);
    };
  }, []);
  if (seconds > 10) {
    timer(true);
  }

  return (
    <AlertBox variant={variant}>
      {icon ? (
        <span className={"mr2"}>
          <FontAwesomeIcon icon={icons[variant].icon} />
        </span>
      ) : undefined}
      {children}
    </AlertBox>
  );
};

export type { IAlertProps };
export { Alert };
