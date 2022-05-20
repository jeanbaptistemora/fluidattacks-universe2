interface IFormValues {
  filename: string | undefined;
  lastAuthor: string | undefined;
  lastCommit: string | undefined;
  loc: number | undefined;
  modifiedDate: Date | undefined;
  rootId: string | undefined;
}

interface IHandleAdditionModalFormProps {
  roots: IGitRootAttr[];
  handleCloseModal: () => void;
}

interface IAddToeInputResultAttr {
  addToeLines: {
    success: boolean;
  };
}

interface IHandleAdditionModalProps {
  groupName: string;
  isAdding: boolean;
  handleCloseModal: () => void;
  refetchData: () => void;
}

interface IGitRootAttr {
  __typename: "GitRoot";
  id: string;
  nickname: string;
  state: "ACTIVE" | "INACTIVE";
}

export type {
  IFormValues,
  IHandleAdditionModalProps,
  IHandleAdditionModalFormProps,
  IAddToeInputResultAttr,
  IGitRootAttr,
};
