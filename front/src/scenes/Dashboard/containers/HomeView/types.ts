export interface IHomeViewProps {
  setUserRole(userRole: string | undefined): void;
}

export interface ITagData {
  name: string;
  projects: Array<{ name: string }>;
}

export interface IUserAttr {
  me: {
    projects: Array<{ description: string; name: string }>;
    tags: ITagData[];
  };
}
