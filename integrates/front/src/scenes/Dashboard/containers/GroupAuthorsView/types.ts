interface IGroupAuthor {
  actor: string;
  commit: string;
  groups: string;
  organization: string;
  repository: string;
}

interface IData {
  group: {
    authors: {
      data: IGroupAuthor[];
    };
  };
}

interface IAuthors extends IGroupAuthor {
  invitation: JSX.Element;
}

export { IAuthors, IGroupAuthor, IData };
