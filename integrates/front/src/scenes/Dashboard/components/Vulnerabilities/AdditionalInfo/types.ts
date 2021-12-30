interface IVulnInfoAttr {
  commitHash: string | null;
  cycles: string;
  efficacy: string;
  hacker?: string;
}

interface IGetVulnAdditionalInfoAttr {
  vulnerability: IVulnInfoAttr;
}

export { IGetVulnAdditionalInfoAttr };
