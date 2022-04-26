import type { IToeInputData } from "../types";

interface IFormValues {
  bePresent: boolean;
  hasRecentAttack: boolean | undefined;
}

interface IHandleEditionModalFormProps {
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
  setSelectedToeInputDatas: (selectedToeInputDatas: IToeInputData[]) => void;
}

export type {
  IFormValues,
  IHandleEditionModalProps,
  IHandleEditionModalFormProps,
  IUpdateToeInputResultAttr,
};
