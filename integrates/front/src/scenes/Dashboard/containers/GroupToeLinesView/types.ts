interface IToeLinesAttr {
  comments: string;
  filename: string;
  loc: number;
  modifiedDate: string;
  modifiedCommit: string;
  testedDate: string;
  testedLines: string;
}

interface IGitRootAttr {
  id: string;
  toeLines: IToeLinesAttr[];
}

interface IToeLinesData {
  comments: string;
  filename: string;
  groupName: string;
  loc: number;
  modifiedDate: string;
  modifiedCommit: string;
  rootId: string;
  testedDate: string;
  testedLines: string;
}

export type { IGitRootAttr, IToeLinesAttr, IToeLinesData };
