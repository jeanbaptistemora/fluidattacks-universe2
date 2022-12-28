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
interface IBasicEnvironmentUrl {
  id: string;
  url: string;
  urlType: string;
}

interface ICredentials {
  auth: "" | "TOKEN" | "USER";
  azureOrganization: string;
  id: string;
  isPat: boolean;
  key: string;
  name: string;
  password: string;
  token: string;
  type: "" | "HTTPS" | "SSH";
  typeCredential: "" | "SSH" | "TOKEN" | "USER";
  user: string;
}
interface ICredentialsAttr {
  id: string;
  isPat: boolean;
  isToken: boolean;
  name: string;
  type: "" | "HTTPS" | "SSH";
}

declare type CloningStatusType = "FAIL" | "N/A" | "OK" | "QUEUED" | "UNKNOWN";

interface IGitRootAttr {
  __typename: "GitRoot";
  branch: string;
  cloningStatus: {
    message: string;
    status: CloningStatusType;
  };
  credentials: ICredentials | null;
  environment: string;
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

interface IGitRootData {
  __typename: "GitRoot";
  branch: string;
  cloningStatus: {
    message: string;
    status: CloningStatusType;
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
    status: CloningStatusType;
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
  CloningStatusType,
  Root,
  IBasicEnvironmentUrl,
  IGitRootAttr,
  IGitRootData,
  IIPRootAttr,
  IURLRootAttr,
  IEnvironmentUrl,
  ISecret,
  ICredentials,
  ICredentialsAttr,
  IUpdateGitEnvironments,
  IFormValues,
};
