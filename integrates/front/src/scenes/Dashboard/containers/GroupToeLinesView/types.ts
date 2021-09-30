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
  toeLines: IToeLinesAttr[];
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
  pendingLines: number;
  rootId: string;
  rootNickname: string;
  sortsRiskLevel: string;
  testedDate: string;
  testedLines: number;
}

export type { IGitRootAttr, IToeLinesAttr, IToeLinesData };
