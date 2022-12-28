interface IAddCredentialsResultAttr {
  addCredentials: {
    success: boolean;
  };
}

interface ICredentialsAttr {
  azureOrganization: string | null;
  id: string;
  isPat: boolean;
  isToken: boolean;
  name: string;
  owner: string;
  type: "HTTPS" | "SSH";
}

interface ICredentialsData {
  azureOrganization: string | null;
  formattedType: string;
  id: string;
  isPat: boolean;
  isToken: boolean;
  name: string;
  owner: string;
  type: "HTTPS" | "SSH";
}

interface IOrganizationAttr {
  id: string;
  name: string;
}

interface IOrganizationCredentialsProps {
  organizationId: string;
}

interface IRemoveCredentialsResultAttr {
  removeCredentials: {
    success: boolean;
  };
}

interface IUpdateCredentialsResultAttr {
  updateCredentials: {
    success: boolean;
  };
}

export type {
  IAddCredentialsResultAttr,
  ICredentialsAttr,
  ICredentialsData,
  IOrganizationAttr,
  IOrganizationCredentialsProps,
  IRemoveCredentialsResultAttr,
  IUpdateCredentialsResultAttr,
};
