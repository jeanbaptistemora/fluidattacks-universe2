interface IFormValues {
  port: string;
  rootId: string;
}

interface IAddToePortResultAttr {
  addToePort: {
    success: boolean;
  };
}

interface IHandleAdditionModalProps {
  groupName: string;
  handleCloseModal: () => void;
  refetchData: () => void;
}

interface IGitRootAttr {
  __typename: "GitRoot";
}

interface IIPRootAttr {
  __typename: "IPRoot";
  address: string;
  id: string;
  nickname: string;
  state: "ACTIVE" | "INACTIVE";
}

interface IURLRootAttr {
  __typename: "URLRoot";
}

type Root = IGitRootAttr | IIPRootAttr | IURLRootAttr;

export type {
  IFormValues,
  IHandleAdditionModalProps,
  IAddToePortResultAttr,
  Root,
  IGitRootAttr,
  IIPRootAttr,
  IURLRootAttr,
};
