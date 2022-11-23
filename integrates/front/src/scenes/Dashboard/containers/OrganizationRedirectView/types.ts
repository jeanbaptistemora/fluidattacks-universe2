interface IOrganizationRedirectProps {
  type: string;
}

interface IGetEntityOrganization {
  group?: {
    name: string;
    organization: string;
  };
  tag?: {
    organization: string;
  };
}

export type { IGetEntityOrganization, IOrganizationRedirectProps };
