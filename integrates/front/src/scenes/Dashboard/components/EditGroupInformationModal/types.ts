export interface IEditGroupInformation {
  initialValues: Record<string, string>;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: () => void;
}
