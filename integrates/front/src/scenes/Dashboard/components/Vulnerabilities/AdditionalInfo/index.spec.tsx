import { AdditionalInfo } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo";
import type { IVulnRowAttr } from "../types";
import React from "react";
import type { ReactWrapper } from "enzyme";
import moment from "moment";
import { mount } from "enzyme";

describe("AdditionalInfo", (): void => {
  const numberOfDays: number = 5;
  const mockVuln: IVulnRowAttr = {
    commitHash: "",
    currentState: "open",
    currentStateCapitalized: "Open",
    cycles: "1",
    efficacy: "0",
    externalBts: "",
    historicTreatment: [
      {
        acceptanceDate: "",
        acceptanceStatus: "",
        date: "2019-07-05 09:56:40",
        justification: "test progress justification",
        treatment: "IN PROGRESS",
        treatmentManager: "treatment-manager-4",
        user: "usertreatment@test.test",
      },
    ],
    id: "af7a48b8-d8fc-41da-9282-d424fff563f0",
    lastReattackDate: moment()
      .subtract(numberOfDays, "days")
      .format("YYYY-MM-DD hh:mm:ss"),
    lastReattackRequester: "",
    lastRequestedReattackDate: "",
    remediated: false,
    reportDate: "",
    severity: "1",
    specific: "specific-3",
    stream: "",
    tag: "tag-7, tag-8",
    treatment: "IN PROGRESS",
    treatmentChanges: 1,
    treatmentDate: "2019-07-05 09:56:40",
    treatmentManager: "treatment-manager-4",
    verification: "Verified",
    vulnType: "lines",
    where: "https://example.com/lines",
    zeroRisk: "",
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof AdditionalInfo).toStrictEqual("function");
  });

  it("should render in vulnerabilities", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <AdditionalInfo canDisplayAnalyst={false} vulnerability={mockVuln} />
    );
    wrapper.update();

    expect(wrapper).toHaveLength(1);
  });
});
