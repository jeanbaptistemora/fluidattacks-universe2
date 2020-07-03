export interface IUserDataAttr {
  user: {
    organization: string;
    phoneNumber: string;
    responsibility: string;
  };
}

export interface IAddUserModalProps {
  initialValues: Record<string, string>;
  open: boolean;
  projectName?: string;
  type: "add" | "edit";
  onClose(): void;
  onSubmit(values: {}): void;
}
