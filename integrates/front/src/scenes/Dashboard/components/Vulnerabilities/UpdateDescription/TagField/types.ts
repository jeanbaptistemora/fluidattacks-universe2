interface ITagFieldProps {
  handleDeletion: (tag: string) => void;
  hasNewVulnSelected: boolean;
  isAcceptedSelected: boolean;
  isAcceptedUndefinedSelected: boolean;
  isInProgressSelected: boolean;
}

export type { ITagFieldProps };
