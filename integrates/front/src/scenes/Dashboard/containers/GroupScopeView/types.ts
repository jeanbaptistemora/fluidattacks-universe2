interface IGitRootAttr {
  __typename: "GitRoot";
  branch: string;
  environment: string;
  filter: {
    paths: string[];
    policy: "EXCLUDE" | "INCLUDE";
  } | null;
  includesHealthCheck: boolean;
  id: string;
  url: string;
}

interface IIPRootAttr {
  __typename: "IPRoot";
  address: string;
  id: string;
  port: number;
}

interface IURLRootAttr {
  __typename: "URLRoot";
  host: string;
  id: string;
  path: string;
  port: number;
  protocol: "HTTP" | "HTTPS";
}

type Root = IGitRootAttr | IIPRootAttr | IURLRootAttr;

interface IGitFormAttr {
  branch: string;
  environment: string;
  filter: {
    paths: string[];
    policy: "EXCLUDE" | "INCLUDE" | "NONE";
  };
  includesHealthCheck: boolean;
  url: string;
}

export type { Root, IGitRootAttr, IGitFormAttr, IIPRootAttr, IURLRootAttr };
