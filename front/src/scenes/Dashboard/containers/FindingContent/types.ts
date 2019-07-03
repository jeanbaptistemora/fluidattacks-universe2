import { RouteComponentProps } from "react-router";

export type IFindingContentBaseProps = Pick<RouteComponentProps<{ findingId: string; projectName: string }>, "match">;

export interface IFindingContentStateProps {
  alert?: string;
  header: {
    closedVulns: number;
    openVulns: number;
    reportDate: string;
    severity: number;
    status: "Abierto" | "Cerrado" | "Default";
  };
  title: string;
}

export interface IFindingContentDispatchProps {
  onApprove(): void;
  onConfirmDelete(): void;
  onDelete(justification: string): void;
  onLoad(): void;
  onReject(): void;
  onUnmount(): void;
  openDeleteConfirm(): void;
  openRejectConfirm(): void;
}

export type IFindingContentProps = IFindingContentBaseProps &
  (IFindingContentStateProps & IFindingContentDispatchProps);
