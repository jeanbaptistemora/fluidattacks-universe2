import type { Moment } from "moment";

import type { IToeLinesData } from "../types";

interface IFormValues {
  attackedAt: Moment;
  attackedLines: number | undefined;
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
}

export {
  IFormValues,
  IHandleEditionModalProps,
  IHandleEditionModalFormProps,
  IUpdateToeLinesAttackedLinesResultAttr,
};
