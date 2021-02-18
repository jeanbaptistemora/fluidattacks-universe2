interface IStakeholderAttrs {
  stakeholder: {
    organization: string;
    phoneNumber: string;
    responsibility: string;
  };
}

interface IAddStakeholderModalProps {
  action: "add" | "edit";
  editTitle: string;
  initialValues: Record<string, string>;
  open: boolean;
  organizationId?: string;
  projectName?: string;
  title: string;
  type: "organization" | "user";
  onClose: () => void;
  // Annotation needed for compatibility with Project and Organization
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onSubmit: (values: any) => void;
}

export { IAddStakeholderModalProps, IStakeholderAttrs };
