export interface IStakeholderDataAttr {
  stakeholder: {
    organization: string;
    phoneNumber: string;
    responsibility: string;
  };
}

export interface IAddStakeholderModalProps {
  action: "add" | "edit";
  editTitle: string;
  initialValues: Record<string, string>;
  open: boolean;
  organizationId?: string;
  projectName?: string;
  title: string;
  type: "organization" | "user";
  onClose(): void;
  onSubmit(values: {}): void;
}
