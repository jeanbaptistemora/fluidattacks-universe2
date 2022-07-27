import type { ICredentialsData } from "./types";

const getCredentialsIndex = (
  selectedCredentials: ICredentialsData[],
  allCredentials: ICredentialsData[]
): number[] => {
  const selectedIds: string[] = selectedCredentials.map(
    (selected: ICredentialsData): string => selected.id
  );

  return allCredentials.reduce(
    (
      selectedIndex: number[],
      currentCredentials: ICredentialsData,
      currentCredentialsIndex: number
    ): number[] =>
      selectedIds.includes(currentCredentials.id)
        ? [...selectedIndex, currentCredentialsIndex]
        : selectedIndex,
    []
  );
};

const getNonSelectableCredentialsIndex: (
  stakeholderEmail: string,
  allCredentials: ICredentialsData[]
) => number[] = (
  stakeholderEmail: string,
  allCredentials: ICredentialsData[]
): number[] => {
  return allCredentials.reduce(
    (
      selectedCredentialsIndex: number[],
      currentCredentials: ICredentialsData,
      currentCredentialsIndex: number
    ): number[] =>
      currentCredentials.owner === stakeholderEmail
        ? selectedCredentialsIndex
        : [...selectedCredentialsIndex, currentCredentialsIndex],
    []
  );
};

export { getCredentialsIndex, getNonSelectableCredentialsIndex };
