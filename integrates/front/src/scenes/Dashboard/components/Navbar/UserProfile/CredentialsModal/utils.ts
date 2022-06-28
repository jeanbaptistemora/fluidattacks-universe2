import type { ICredentialData } from "./types";

const getCredentialsId: (credentials: ICredentialData) => string = (
  credentials: ICredentialData
): string => credentials.organizationId + credentials.id;

const getCredentialsIds: (credentialsDatas: ICredentialData[]) => string[] = (
  credentialsDatas: ICredentialData[]
): string[] =>
  credentialsDatas.map((credentialsData: ICredentialData): string =>
    getCredentialsId(credentialsData)
  );

const getCredentialsIndex: (
  selectedCredentialsDatas: ICredentialData[],
  allCredentialsDatas: ICredentialData[]
) => number[] = (
  selectedCredentialsDatas: ICredentialData[],
  allCredentialsDatas: ICredentialData[]
): number[] => {
  const selectCredentialsIds: string[] = getCredentialsIds(
    selectedCredentialsDatas
  );

  return allCredentialsDatas.reduce(
    (
      selectedCredentialsIndex: number[],
      currentCredentialsData: ICredentialData,
      currentCredentialsDataIndex: number
    ): number[] =>
      selectCredentialsIds.includes(getCredentialsId(currentCredentialsData))
        ? [...selectedCredentialsIndex, currentCredentialsDataIndex]
        : selectedCredentialsIndex,
    []
  );
};

const onSelectSeveralCredentialsHelper = (
  isSelect: boolean,
  credentialsDatasSelected: ICredentialData[],
  selectedCredentialsDatas: ICredentialData[],
  setSelectedCredentials: (
    value: React.SetStateAction<ICredentialData[]>
  ) => void
): string[] => {
  if (isSelect) {
    const credentialsToSet: ICredentialData[] = Array.from(
      new Set([...selectedCredentialsDatas, ...credentialsDatasSelected])
    );
    setSelectedCredentials(credentialsToSet);

    return credentialsToSet.map((credentialsData: ICredentialData): string =>
      getCredentialsId(credentialsData)
    );
  }
  const credentialsIds: string[] = getCredentialsIds(credentialsDatasSelected);
  setSelectedCredentials(
    Array.from(
      new Set(
        selectedCredentialsDatas.filter(
          (selectedcredentialsData: ICredentialData): boolean =>
            !credentialsIds.includes(getCredentialsId(selectedcredentialsData))
        )
      )
    )
  );

  return selectedCredentialsDatas.map(
    (credentialsData: ICredentialData): string =>
      getCredentialsId(credentialsData)
  );
};

export { getCredentialsIndex, onSelectSeveralCredentialsHelper };
