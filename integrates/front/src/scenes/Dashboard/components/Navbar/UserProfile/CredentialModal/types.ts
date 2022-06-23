interface IAddCredentialsResultAttr {
  addCredentials: {
    success: boolean;
  };
}

interface ICredentialAttr {
  id: string;
  name: string;
  type: string;
  organization: {
    id: string;
    name: string;
  };
}

interface ICredentialData {
  id: string;
  name: string;
  type: string;
  organization: {
    id: string;
    name: string;
  };
  organizationId: string;
  organizationName: string;
}

interface ICredentialModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface IOrganizationAttr {
  id: string;
  name: string;
}

interface IRemoveCredentialsResultAttr {
  removeCredentials: {
    success: boolean;
  };
}

export type {
  IAddCredentialsResultAttr,
  ICredentialAttr,
  ICredentialData,
  ICredentialModalProps,
  IOrganizationAttr,
  IRemoveCredentialsResultAttr,
};
