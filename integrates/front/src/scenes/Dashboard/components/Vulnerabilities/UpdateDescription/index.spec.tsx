import type { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  getLastTreatment,
  groupLastHistoricTreatment,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

describe("Update Description component", () => {

  it("should group last treatment", async () => {
    const treatment: IHistoricTreatment = {
      date: "",
      justification: "test justification",
      treatment: "IN PROGRESS",
      user: "",
    };

    const vulnerabilities: IVulnDataType[] = [
      {
        currentState: "",
        externalBts: "",
        historicTreatment: [treatment],
        id: "test_one",
        severity: "",
        specific: "",
        tag: "one",
        treatmentManager: "",
        where: "",
      },
      {
        currentState: "",
        externalBts: "",
        historicTreatment: [treatment],
        id: "test_two",
        severity: "",
        specific: "",
        tag: "one",
        treatmentManager: "",
        where: "",
      },
    ];

    const lastTreatment: IHistoricTreatment = groupLastHistoricTreatment(vulnerabilities);

    expect(lastTreatment)
      .toEqual(getLastTreatment([treatment]));
  });
});
