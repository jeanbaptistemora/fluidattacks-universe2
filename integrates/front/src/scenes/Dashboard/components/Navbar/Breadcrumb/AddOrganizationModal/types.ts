interface IAddOrganizationModalProps {
  open: boolean;
  onClose: () => void;
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

export type { IAddOrganizationModalProps, IAddOrganizationMtProps };
