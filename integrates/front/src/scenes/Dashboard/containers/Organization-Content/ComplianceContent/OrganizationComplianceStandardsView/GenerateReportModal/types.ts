import type { IUnfulfilledStandardAttr } from "../types";

interface IGenerateReportModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  unfulfilledStandards: IUnfulfilledStandardAttr[];
}

interface ITableRowData extends IUnfulfilledStandardAttr {
  include: boolean;
}

export type { IGenerateReportModalProps, ITableRowData };
