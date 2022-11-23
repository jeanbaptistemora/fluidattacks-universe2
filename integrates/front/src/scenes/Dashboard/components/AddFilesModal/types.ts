export interface IAddFilesModalProps {
  isOpen: boolean;
  isUploading: boolean;
  onClose: () => void;
  onSubmit: (values: { description: string; file: FileList }) => void;
}
