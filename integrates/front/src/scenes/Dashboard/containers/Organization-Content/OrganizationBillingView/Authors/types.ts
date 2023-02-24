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
  actor: string;
  activeGroups: string;
}

export type {
  IGetOrganizationBilling,
  IOrganizationActiveGroupAttr,
  IOrganizationAuthorAttr,
  IOrganizationAuthorsTable,
};
