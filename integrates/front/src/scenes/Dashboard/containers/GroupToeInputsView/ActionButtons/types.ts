interface IActionButtonsProps {
  areInputsSelected: boolean;
  isAdding: boolean;
  isEnumeratingMode: boolean;
  isInternal: boolean;
  isRemovingMode: boolean;
  onAdd: () => void;
  onEnumerate: () => void;
  onEnumerateMode: () => void;
  onRemove: () => void;
  onRemoveMode: () => void;
}

export { IActionButtonsProps };
