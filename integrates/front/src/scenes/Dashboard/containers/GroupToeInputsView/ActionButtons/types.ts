interface IActionButtonsProps {
  areInputsSelected: boolean;
  isAdding: boolean;
  isMarkingAsAttacked: boolean;
  isEditing: boolean;
  isInternal: boolean;
  onAdd: () => void;
  onMarkAsAttacked: () => void;
  onEdit: () => void;
}

export type { IActionButtonsProps };
