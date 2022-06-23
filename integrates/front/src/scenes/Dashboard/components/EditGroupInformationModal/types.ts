export interface IEditGroupInformation {
  initialValues: Record<string, boolean | string>;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: Record<string, boolean | string>) => void;
}
