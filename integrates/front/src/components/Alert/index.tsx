/* eslint-disable react/require-default-props */
import type { IconDefinition } from "@fortawesome/fontawesome-common-types";
import {
  faCheckCircle,
  faCircleExclamation,
  faCircleInfo,
  faTriangleExclamation,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { Dispatch, FC, ReactNode, SetStateAction } from "react";
import React, { useCallback, useEffect, useState } from "react";

import type { IAlertBoxProps, TAlertVariant } from "./Box";
import { AlertBox } from "./Box";

import { Button } from "components/Button";
import { Gap } from "components/Layout";

interface IAlertProps extends IAlertBoxProps {
  autoHide?: boolean;
  children: ReactNode;
  closable?: boolean;
  icon?: boolean;
  time?: 4 | 8 | 12;
  onTimeOut?: Dispatch<SetStateAction<boolean>>;
}

interface IIcons {
  icon: IconDefinition;
}

const icons: Record<TAlertVariant, IIcons> = {
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

const Alert: FC<IAlertProps> = ({
  autoHide = false,
  children,
  closable = false,
  icon = false,
  onTimeOut: timer,
  show = true,
  time = 8,
  variant = "error",
}: Readonly<IAlertProps>): JSX.Element | null => {
  const [showBox, setShowBox] = useState(show);
  const handleHide = useCallback((): void => {
    setShowBox(false);
  }, []);
  useEffect((): VoidFunction => {
    const timeout = setTimeout((): void => {
      timer?.(true);
      if (autoHide) {
        handleHide();
      }
    }, time * 1000);

    return (): void => {
      clearTimeout(timeout);
    };
  }, [autoHide, handleHide, time, timer]);
  useEffect((): void => {
    setShowBox(show);
  }, [show, setShowBox]);

  return (
    <AlertBox show={showBox} variant={variant}>
      <Gap>
        {icon ? <FontAwesomeIcon icon={icons[variant].icon} /> : undefined}
        {children}
      </Gap>
      {closable ? (
        <Button onClick={handleHide} size={"sm"}>
          <FontAwesomeIcon icon={faXmark} />
        </Button>
      ) : undefined}
    </AlertBox>
  );
};

export type { IAlertProps };
export { Alert };
