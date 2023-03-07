/* eslint-disable fp/no-mutation */
import type { DiagnosticSeverity, Range } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { Diagnostic } from "vscode";

interface IGroup {
  name: string;
  subscription: string;
}

interface IOrganization {
  groups: IGroup[];
}

interface IGitRoot {
  id: string;
  nickname: string;
  groupName: string;
  state: "ACTIVE" | "INACTIVE";
  gitignore: string[];
  downloadUrl?: string;
  url?: string;
  gitEnvironmentUrls: {
    id: string;
    url: string;
  }[];
}
interface IToeLineNode {
  attackedLines: number;
  filename: string;
  comments: string;
  modifiedDate: string;
  loc: number;
  fileExists?: boolean;
}
interface IEdge {
  node: IToeLineNode;
}
interface IToeLinesPaginator {
  edges: IEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}

interface IVulnerability {
  id: string;
  specific: string;
  where: string;
  rootNickname: string;
  state: "REJECTED" | "SAFE" | "SUBMITTED" | "VULNERABLE";
  finding: IFinding;
}

interface IFinding {
  description: string;
  id: string;
  title: string;
}
class VulnerabilityDiagnostic extends Diagnostic {
  public vulnerabilityId?: string;

  public findingId?: string;

  public constructor(
    findingId: string,
    vulnId: string,
    range: Range,
    message: string,
    severity?: DiagnosticSeverity
  ) {
    super(range, message, severity);

    this.vulnerabilityId = vulnId;
    this.findingId = findingId;
  }
}

export type {
  IGroup as Group,
  IOrganization as Organization,
  IGitRoot,
  IToeLinesPaginator,
  IEdge,
  IToeLineNode,
  IVulnerability,
  IFinding,
};

export { VulnerabilityDiagnostic };
