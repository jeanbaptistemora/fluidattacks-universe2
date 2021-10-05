interface IToeInputAttr {
  commit: string;
  component: string;
  createdDate: string;
  entryPoint: string;
  seenFirstTimeBy: string;
  testedDate: string;
  unreliableRootNickname: string;
  verified: string;
  vulnerabilities: string;
}

interface IToeInputData {
  commit: string;
  component: string;
  createdDate: string;
  entryPoint: string;
  seenFirstTimeBy: string;
  testedDate: string;
  unreliableRootNickname: string;
  verified: string;
  vulnerabilities: string;
}

export type { IToeInputAttr, IToeInputData };
