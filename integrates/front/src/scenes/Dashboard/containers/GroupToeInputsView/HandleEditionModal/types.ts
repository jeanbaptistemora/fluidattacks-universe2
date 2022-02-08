import type { Moment } from "moment";

import type { IToeInputData } from "../types";

interface IFormValues {
  attackedAt: Moment;
  bePresent: boolean;
}

interface IHandleEditionModalFormProps {
  selectedToeInputDatas: IToeInputData[];
  handleCloseModal: () => void;
}

interface IUpdateToeInputResultAttr {
  updateToeInput: {
    success: boolean;
  };
}

interface IHandleEditionModalProps {
  groupName: string;
  selectedToeInputDatas: IToeInputData[];
  handleCloseModal: () => void;
  refetchData: () => void;
}

export {
  IFormValues,
  IHandleEditionModalProps,
  IHandleEditionModalFormProps,
  IUpdateToeInputResultAttr,
};
