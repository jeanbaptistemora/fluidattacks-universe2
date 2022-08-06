/* eslint-disable react/require-default-props */
import { faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { Dispatch, FC, ReactNode, SetStateAction } from "react";
import React, { useCallback, useEffect, useState } from "react";

import type { IAlertBoxProps } from "./Box";
import { AlertBox, ContentBox, variants } from "./Box";

import { Button } from "components/Button";

interface IAlertProps extends IAlertBoxProps {
  autoHide?: boolean;
  children: ReactNode;
  closable?: boolean;
  time?: 4 | 8 | 12;
  onTimeOut?: Dispatch<SetStateAction<boolean>>;
}

const Alert: FC<IAlertProps> = ({
  autoHide = false,
  children,
  closable = false,
  onTimeOut: timer,
  show = true,
  time = 8,
  variant = "error",
}: Readonly<IAlertProps>): JSX.Element => {
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
      <FontAwesomeIcon icon={variants[variant].icon} />
      <ContentBox>{children}</ContentBox>
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
