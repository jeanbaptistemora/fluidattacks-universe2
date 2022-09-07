/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { ToastOptions } from "react-toastify";
import { Slide, toast as toastify } from "react-toastify";

import type { IToastBoxProps } from "./ToastBox";
import { ToastBox } from "./ToastBox";

import type { IAlertBoxProps } from "../Box";
import { AlertBox, ContentBox, variants } from "../Box";
import { Text } from "components/Text";

interface IToastProps
  extends Pick<IAlertBoxProps, "variant">,
    Pick<ToastOptions, "autoClose" | "closeButton" | "delay" | "draggable"> {
  msg: string;
  title: string;
}

const toast = ({
  autoClose,
  closeButton,
  delay,
  draggable,
  msg,
  title,
  variant = "error",
}: Readonly<IToastProps>): void => {
  const id = title.toLowerCase() + msg.toLowerCase();
  toastify.dismiss(id);
  toastify(
    <AlertBox show={true} variant={variant}>
      <FontAwesomeIcon icon={variants[variant].icon} />
      <ContentBox>
        <Text fw={7} mb={1} size={3} tone={"dark"}>
          {title}
        </Text>
        <Text size={3} tone={"dark"}>
          {msg}
        </Text>
      </ContentBox>
    </AlertBox>,
    {
      autoClose,
      closeButton,
      delay,
      draggable,
      toastId: id,
      transition: Slide,
    }
  );
};

export type { IToastBoxProps, IToastProps };
export { ToastBox, toast };
