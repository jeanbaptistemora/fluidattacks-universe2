import { RouteComponentProps } from "react-router";

export type IFindingContentBaseProps = Pick<RouteComponentProps<{ findingId: string; projectName: string }>, "match">;

export interface IFindingContentStateProps {
  alert?: string;
  userRole: string;
}

export interface IFindingContentDispatchProps {
  onApprove(): void;
  onConfirmDelete(): void;
  onDelete(justification: string): void;
  onLoad(): void;
  onReject(): void;
  onUnmount(): void;
}

export interface IHeaderQueryResult {
  finding: {
    analyst?: string;
    closedVulns: number;
    historicState: Array<{
      analyst: string; date: string; state: string;
    }>;
    id: string;
    openVulns: number;
    releaseDate: string;
    reportDate: string;
    severityScore: number;
    state: "open" | "closed" | "default";
    title: string;
  };
}

export type IFindingContentProps = IFindingContentBaseProps &
  (IFindingContentStateProps & IFindingContentDispatchProps);
