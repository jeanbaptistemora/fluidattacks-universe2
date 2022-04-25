interface IAddOrganizationModalProps {
  open: boolean;
  onClose: () => void;
}

interface IAddOrganizationQryProps {
  internalNames: {
    name: string;
  };
}

interface IAddOrganizationMtProps {
  addOrganization: {
    organization: {
      id: string;
      name: string;
    };
    success: boolean;
  };
}

export type {
  IAddOrganizationModalProps,
  IAddOrganizationMtProps,
  IAddOrganizationQryProps,
};
