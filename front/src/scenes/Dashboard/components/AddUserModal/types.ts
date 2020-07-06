export interface IUserDataAttr {
  user: {
    organization: string;
    phoneNumber: string;
    responsibility: string;
  };
}

export interface IAddUserModalProps {
  action: "add" | "edit";
  editTitle: string;
  initialValues: Record<string, string>;
  open: boolean;
  organizationName?: string;
  projectName?: string;
  title: string;
  type: "organization" | "user";
  onClose(): void;
  onSubmit(values: {}): void;
}
