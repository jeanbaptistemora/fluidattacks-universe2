import type { Moment } from "moment";

import type { IToeLinesData } from "../types";

interface IFormValues {
  attackedAt: Moment;
  attackedLines: number | undefined;
  comments: string;
}

interface IHandleEditModalFormProps {
  selectedToeLinesDatas: IToeLinesData[];
  handleCloseModal: () => void;
}

interface IUpdateToeLinesAttackedLinesResultAttr {
  updateToeLinesAttackedLines: {
    success: boolean;
  };
}

interface IHandleEditModalProps {
  groupName: string;
  selectedToeLinesDatas: IToeLinesData[];
  handleCloseModal: () => void;
}

export {
  IFormValues,
  IHandleEditModalProps,
  IHandleEditModalFormProps,
  IUpdateToeLinesAttackedLinesResultAttr,
};
