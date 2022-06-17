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
  organizationName: string;
}

interface ICredentialModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export type { ICredentialAttr, ICredentialData, ICredentialModalProps };
