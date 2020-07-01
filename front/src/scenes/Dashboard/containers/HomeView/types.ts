export interface IHomeViewProps {
  setUserRole(userRole: string | undefined): void;
}

export interface IOrganizationData {
  id: string;
  name: string;
}

export interface ITagData {
  name: string;
  projects: Array<{ name: string }>;
}

export interface IUserAttr {
  me: {
    organizations: IOrganizationData[];
    projects: Array<{ description: string; name: string }>;
    tags: ITagData[];
  };
}
