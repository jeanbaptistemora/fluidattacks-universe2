export interface IAddOrganizationModalProps {
  open: boolean;
  onClose(): void;
}

export interface IAddOrganizationQryResult {
  internalNames: {
    name: string;
  };
}

export interface IAddOrganizationMtResult {
  createOrganization: {
    organization: {
      id: string;
      name: string;
    };
    success: boolean;
  };
}
