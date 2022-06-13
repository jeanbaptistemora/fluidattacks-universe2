interface ISecret {
  description: string;
  key: string;
  value: string;
}
interface IEnvironmentUrl {
  cloudName: string | undefined;
  id: string;
  url: string;
  secrets: ISecret[];
  createdAt: string;
  urlType: string;
}
interface ICredentials {
  id: string;
  key: string;
  name: string;
  password: string;
  token: string;
  type: "" | "HTTPS" | "SSH";
  user: string;
}
interface IGitRootAttr {
  __typename: "GitRoot";
  branch: string;
  cloningStatus: {
    message: string;
    status: "FAIL" | "N/A" | "OK" | "QUEUED" | "UNKNOWN";
  };
  credentials: ICredentials | null;
  environment: string;
  environmentUrls: string[];
  gitEnvironmentUrls: IEnvironmentUrl[];
  gitignore: string[];
  healthCheckConfirm: string[] | undefined;
  includesHealthCheck: boolean | null;
  id: string;
  nickname: string;
  secrets: ISecret[];
  state: "ACTIVE" | "INACTIVE";
  url: string;
  useVpn: boolean;
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
  query: string | null;
  state: "ACTIVE" | "INACTIVE";
}

interface IUpdateGitEnvironments extends IGitRootAttr {
  reason?: string;
  other?: string;
}

type Root = IGitRootAttr | IIPRootAttr | IURLRootAttr;

interface IFormValues {
  branch: string;
  cloningStatus: {
    message: string;
    status: "FAIL" | "N/A" | "OK" | "QUEUED" | "UNKNOWN";
  };
  credentials: ICredentials;
  environment: string;
  environmentUrls: string[];
  gitEnvironmentUrls: IEnvironmentUrl[];
  gitignore: string[];
  healthCheckConfirm: string[] | undefined;
  includesHealthCheck: boolean | null;
  id: string;
  nickname: string;
  secrets: ISecret[];
  state: "ACTIVE" | "INACTIVE";
  url: string;
  useVpn: boolean;
}

export type {
  Root,
  IGitRootAttr,
  IIPRootAttr,
  IURLRootAttr,
  IEnvironmentUrl,
  ISecret,
  ICredentials,
  IUpdateGitEnvironments,
  IFormValues,
};
