import type { ICredentialsData } from "../types";

interface IActionButtonsProps {
  isAdding: boolean;
  isEditing: boolean;
  isRemoving: boolean;
  onAdd: () => void;
  onEdit: () => void;
  onRemove: () => void;
  organizationId: string;
  selectedCredentials: ICredentialsData | undefined;
  shouldDisplayGithubButton: boolean;
  shouldDisplayGitlabButton: boolean;
}

export type { IActionButtonsProps };
