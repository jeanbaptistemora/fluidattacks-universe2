interface IToeLinesAttr {
  comments: string;
  filename: string;
  loc: number;
  modifiedDate: string;
  modifiedCommit: string;
  sortsRiskLevel: string;
  testedDate: string;
  testedLines: number;
}

interface IGitRootAttr {
  id: string;
  nickname: string;
  servicesToeLines: IToeLinesAttr[];
}

interface IToeLinesData {
  attacked: string;
  comments: string;
  coverage: number;
  filename: string;
  groupName: string;
  loc: number;
  modifiedDate: string;
  modifiedCommit: string;
  rootId: string;
  rootNickname: string;
  sortsRiskLevel: string;
  testedDate: string;
  testedLines: number;
}

export type { IGitRootAttr, IToeLinesAttr, IToeLinesData };
