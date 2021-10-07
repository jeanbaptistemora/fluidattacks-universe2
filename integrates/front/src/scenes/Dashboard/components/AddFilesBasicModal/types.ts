export interface IAddFilesBasicModalProps {
  isOpen: boolean;
  isUploading: boolean;
  onClose: () => void;
  onSubmit: (values: { file: FileList }) => void;
}
