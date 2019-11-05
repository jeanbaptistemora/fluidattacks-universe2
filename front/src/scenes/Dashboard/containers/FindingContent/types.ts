import { RouteComponentProps } from "react-router";

export type IFindingContentBaseProps = Pick<RouteComponentProps<{ findingId: string; projectName: string }>, "match">;

export interface IFindingContentStateProps {
  alert?: string;
  header: {
    closedVulns: number;
    openVulns: number;
    reportDate: string;
    severity: number;
    status: "open" | "closed" | "default";
  };
  title: string;
  userRole: string;
}

export interface IFindingContentDispatchProps {
  onApprove(): void;
  onConfirmDelete(): void;
  onDelete(justification: string): void;
  onLoad(): void;
  onReject(): void;
  onUnmount(): void;
  openApproveConfirm(): void;
  openDeleteConfirm(): void;
  openRejectConfirm(): void;
}

export interface IHeaderQueryResult {
  finding: {
    analyst?: string;
    closedVulns: number;
    id: string;
    openVulns: number;
    releaseDate: string;
    reportDate: string;
    submissionHistory: Array<{
      analyst: string; creation_date?: string;
      report_date?: string; review_date?: string;
      reviewer?: string; status?: string;
    }>;
    title: string;
  };
}

export type IFindingContentProps = IFindingContentBaseProps &
  (IFindingContentStateProps & IFindingContentDispatchProps);
