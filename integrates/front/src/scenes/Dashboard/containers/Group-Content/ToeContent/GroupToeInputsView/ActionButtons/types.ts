interface IActionButtonsProps {
  areInputsSelected: boolean;
  isAdding: boolean;
  isMarkingAsAttacked: boolean;
  isInternal: boolean;
  onAdd: () => void;
  onMarkAsAttacked: () => void;
}

export type { IActionButtonsProps };
