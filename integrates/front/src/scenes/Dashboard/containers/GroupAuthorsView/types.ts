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

interface IAuthorInvitation extends IGroupAuthor {
  invitation: JSX.Element;
}

export { IAuthorInvitation, IGroupAuthor, IData };
