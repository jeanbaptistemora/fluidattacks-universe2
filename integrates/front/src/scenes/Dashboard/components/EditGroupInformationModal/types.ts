export interface IEditGroupInformation {
  initialValues: Record<string, string>;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: Record<string, string>) => void;
}
