interface IFormValues {
  component: string;
  entryPoint: string;
  environmentUrl: string | undefined;
  rootId: string | undefined;
}

interface IHandleAdditionModalFormProps {
  roots: Root[];
  handleCloseModal: () => void;
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
  branch: string;
  cloningStatus: {
    message: string;
    status: "FAIL" | "OK" | "UNKNOWN";
  };
  credentials: {
    id: string;
    key: string;
    name: string;
    type: "" | "SSH";
  };
  environment: string;
  environmentUrls: string[];
  gitignore: string[];
  includesHealthCheck: boolean;
  id: string;
  nickname: string;
  state: "ACTIVE" | "INACTIVE";
  url: string;
}

interface IIPRootAttr {
  __typename: "IPRoot";
  address: string;
  id: string;
  nickname: string;
  port: number;
  state: "ACTIVE" | "INACTIVE";
}

interface IURLRootAttr {
  __typename: "URLRoot";
  host: string;
  id: string;
  nickname: string;
  path: string;
  port: number;
  protocol: "HTTP" | "HTTPS";
  state: "ACTIVE" | "INACTIVE";
}

type Root = IGitRootAttr | IIPRootAttr | IURLRootAttr;

export {
  IFormValues,
  IHandleAdditionModalProps,
  IHandleAdditionModalFormProps,
  IAddToeInputResultAttr,
  Root,
  IGitRootAttr,
  IIPRootAttr,
  IURLRootAttr,
};
