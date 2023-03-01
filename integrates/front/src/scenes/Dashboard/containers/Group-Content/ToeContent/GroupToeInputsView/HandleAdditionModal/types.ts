interface IFormValues {
  entryPoint: string;
  environmentUrl: string;
  path: string;
  rootId: string | undefined;
  rootNickname: string | undefined;
}

interface IHandleAdditionModalFormProps {
  roots: Root[];
  host: string | undefined;
  handleCloseModal: () => void;
  setHost: (host: string | undefined) => void;
}

interface IAddToeInputResultAttr {
  addToeInput: {
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
  gitEnvironmentUrls: { url: string; id: string; urlType: string }[];
  id: string;
  nickname: string;
  state: "ACTIVE" | "INACTIVE";
}

interface IIPRootAttr {
  __typename: "IPRoot";
  id: string;
  nickname: string;
}

interface IURLRootAttr {
  __typename: "URLRoot";
  host: string;
  id: string;
  nickname: string;
  path: string;
  port: number;
  protocol: "HTTP" | "HTTPS";
  query: string | null;
  state: "ACTIVE" | "INACTIVE";
}

type Root = IGitRootAttr | IIPRootAttr | IURLRootAttr;

export type {
  IFormValues,
  IHandleAdditionModalProps,
  IHandleAdditionModalFormProps,
  IAddToeInputResultAttr,
  Root,
  IGitRootAttr,
  IIPRootAttr,
  IURLRootAttr,
};
