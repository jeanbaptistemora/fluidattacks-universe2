interface IGitRootAttr {
  __typename: "GitRoot";
  branch: string;
  directoryFiltering?: {
    paths: string[];
    policy: "EXCLUDE" | "INCLUDE";
  };
  environment: {
    kind: string;
    url?: string;
  };
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

export type { Root, IGitRootAttr, IIPRootAttr, IURLRootAttr };
