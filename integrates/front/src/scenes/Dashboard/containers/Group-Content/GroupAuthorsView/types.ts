interface IGroupAuthor {
  actor: string;
  commit: string;
  groups: string;
  organization: string;
  repository: string;
}

interface IData {
  group: {
    billing: {
      authors: IGroupAuthor[];
    };
  };
}

interface IAuthors extends IGroupAuthor {
  invitation: JSX.Element;
}

export type { IAuthors, IGroupAuthor, IData };
