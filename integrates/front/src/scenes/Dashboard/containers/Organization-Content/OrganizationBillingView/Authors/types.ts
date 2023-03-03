interface IOrganizationActorAttr {
  name: string;
  email: string;
}

interface IOrganizationActiveGroupAttr {
  name: string;
  tier: string;
}

interface IOrganizationAuthorAttr {
  actor: string;
  activeGroups: IOrganizationActiveGroupAttr[];
}

interface IGetOrganizationBilling {
  organization: {
    billing: {
      authors: IOrganizationAuthorAttr[];
    };
  };
}

interface IOrganizationAuthorsTable {
  actorName: string;
  actorEmail: string | undefined;
  groupsAuthors: string;
}

export type {
  IGetOrganizationBilling,
  IOrganizationActiveGroupAttr,
  IOrganizationActorAttr,
  IOrganizationAuthorAttr,
  IOrganizationAuthorsTable,
};
