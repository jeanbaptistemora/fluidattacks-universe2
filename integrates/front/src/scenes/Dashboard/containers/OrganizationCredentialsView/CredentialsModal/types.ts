interface IAddCredentialsResultAttr {
  addCredentials: {
    success: boolean;
  };
}

interface ICredentialModalProps {
  isAdding: boolean;
  isEditing: boolean;
  organizationId: string;
  onClose: () => void;
}

interface IUpdateCredentialsResultAttr {
  updateCredentials: {
    success: boolean;
  };
}

export type {
  IAddCredentialsResultAttr,
  ICredentialModalProps,
  IUpdateCredentialsResultAttr,
};
