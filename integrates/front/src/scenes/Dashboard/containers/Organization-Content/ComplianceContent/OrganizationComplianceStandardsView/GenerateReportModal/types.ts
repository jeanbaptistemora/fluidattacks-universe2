import type { IUnfulfilledStandardAttr } from "../types";

interface IGenerateReportModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  unfulfilledStandards: IUnfulfilledStandardAttr[];
}

interface IUnfulfilledStandardData extends IUnfulfilledStandardAttr {
  include: boolean;
}

export type { IGenerateReportModalProps, IUnfulfilledStandardData };
