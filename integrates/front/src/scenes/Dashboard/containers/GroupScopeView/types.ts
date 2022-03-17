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
    password: string;
    token: string;
    type: "" | "HTTPS" | "SSH";
    user: string;
  };
  environment: string;
  environmentUrls: string[];
  gitignore: string[];
  includesHealthCheck: boolean | null;
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

export type { Root, IGitRootAttr, IIPRootAttr, IURLRootAttr };
