export interface IAddFilesModalProps {
  isOpen: boolean;
  isUploading: boolean;
  uploadProgress: number;
  onClose: () => void;
  onSubmit: (values: { description: string; file: FileList }) => void;
}
