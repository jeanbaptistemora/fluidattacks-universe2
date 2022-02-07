interface IActionButtonsProps {
  areInputsSelected: boolean;
  isAdding: boolean;
  isEnumeratingMode: boolean;
  isInternal: boolean;
  onAdd: () => void;
  onEnumerate: () => void;
  onEnumerateMode: () => void;
}

export { IActionButtonsProps };
