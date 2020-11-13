import { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IUpdateTreatmentModal {
  findingId: string;
  lastTreatment?: IHistoricTreatment;
  projectName?: string;
  vulnerabilities: IVulnDataType[];
  handleCloseModal(): void;
}

export { IUpdateTreatmentModal };
