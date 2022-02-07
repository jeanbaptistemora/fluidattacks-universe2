import type { IToeInputData } from "../types";

interface IFormValues {
  seenFirstTimeBy: string | undefined;
}

interface IHandleEnumerationModalFormProps {
  validStakeholders: IStakeholderAttr[];
  handleCloseModal: () => void;
}

interface IEnumerateToeInputResultAttr {
  enumerateToeInput: {
    success: boolean;
  };
}

interface IHandleEnumerationModalProps {
  groupName: string;
  selectedToeInputDatas: IToeInputData[];
  handleCloseModal: () => void;
  refetchData: () => void;
  setSelectedToeInputDatas: (selectedToeInputDatas: IToeInputData[]) => void;
}
interface IGetStakeholdersAttr {
  group: {
    name: string;
    stakeholders: IStakeholderAttr[];
  };
}

interface IStakeholderAttr {
  email: string;
  role: string;
}

export {
  IFormValues,
  IHandleEnumerationModalProps,
  IHandleEnumerationModalFormProps,
  IEnumerateToeInputResultAttr,
  IGetStakeholdersAttr,
  IStakeholderAttr,
};
