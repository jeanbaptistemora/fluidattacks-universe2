interface IVulnInfoAttr {
  commitHash: string | null;
  cycles: string;
  efficacy: string;
  hacker?: string;
  lastReattackRequester: string;
  lastRequestedReattackDate: string | null;
}

interface IGetVulnAdditionalInfoAttr {
  vulnerability: IVulnInfoAttr;
}

export { IGetVulnAdditionalInfoAttr };
