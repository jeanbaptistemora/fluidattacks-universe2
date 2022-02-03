interface IActionButtonsProps {
  areInputsSelected: boolean;
  isAdding: boolean;
  isEnumerating: boolean;
  isInternal: boolean;
  isRemoving: boolean;
  onAdd: () => void;
  onEnumerateMode: () => void;
  onRemove: () => void;
  onRemoveMode: () => void;
}

export { IActionButtonsProps };
