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

export { IGroupAuthor, IData };
