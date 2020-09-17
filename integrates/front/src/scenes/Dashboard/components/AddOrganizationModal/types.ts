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
  createOrganization: {
    organization: {
      id: string;
      name: string;
    };
    success: boolean;
  };
}

export {
  IAddOrganizationModalProps,
  IAddOrganizationMtProps,
  IAddOrganizationQryProps,
};
