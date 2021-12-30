interface IVulnInfoAttr {
  commitHash: string | null;
  cycles: string;
  efficacy: string;
}

interface IGetVulnAdditionalInfoAttr {
  vulnerability: IVulnInfoAttr;
}

export { IGetVulnAdditionalInfoAttr };
