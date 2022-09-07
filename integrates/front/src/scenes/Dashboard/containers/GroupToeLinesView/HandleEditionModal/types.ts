/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IToeLinesData } from "../types";

interface IFormValues {
  attackedLines: number | string;
  comments: string;
}

interface IHandleEditionModalFormProps {
  selectedToeLinesDatas: IToeLinesData[];
  handleCloseModal: () => void;
}

interface IUpdateToeLinesAttackedLinesResultAttr {
  updateToeLinesAttackedLines: {
    success: boolean;
  };
}

interface IHandleEditionModalProps {
  groupName: string;
  selectedToeLinesDatas: IToeLinesData[];
  handleCloseModal: () => void;
  refetchData: () => void;
  setSelectedToeLinesDatas: (selectedToeLinesDatas: IToeLinesData[]) => void;
}

export type {
  IFormValues,
  IHandleEditionModalProps,
  IHandleEditionModalFormProps,
  IUpdateToeLinesAttackedLinesResultAttr,
};
