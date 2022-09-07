/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FC } from "react";
import React from "react";
import type { ToastContainerProps } from "react-toastify";
import { ToastContainer } from "react-toastify";
import styled from "styled-components";

import { CloseToast } from "./CloseToast";

type IToastBoxProps = Pick<
  ToastContainerProps,
  "autoClose" | "closeButton" | "closeOnClick" | "hideProgressBar" | "position"
>;

const StyledToastBox = styled(ToastContainer)`
  > .Toastify__toast {
    border-radius: 4px;
    margin-bottom: 6px;
    padding: 0;
    position: relative;

    .comp-alert {
      padding: 20px 12px;
    }

    > .comp-button {
      position: absolute;
      right: 6px;
      top: 6px;
    }
  }
`;

const ToastBox: FC<IToastBoxProps> = ({
  autoClose = 5000,
  position = "top-right",
}: Readonly<IToastBoxProps>): JSX.Element => (
  <StyledToastBox
    autoClose={autoClose}
    closeButton={<CloseToast closeToast={false} />}
    closeOnClick={false}
    hideProgressBar={true}
    position={position}
  />
);

export type { IToastBoxProps };
export { ToastBox };
