import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import moment from "moment";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IVulnRowAttr } from "../types";
import {
  AdditionalInfo,
  Label,
} from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo";
import { formatVulnerabilities } from "scenes/Dashboard/components/Vulnerabilities/utils";

describe("AdditionalInfo", (): void => {
  const numberOfDays: number = 5;
  const mockVuln: IVulnRowAttr = {
    assigned: "assigned-user-4",
    commitHash: undefined,
    currentState: "open",
    currentStateCapitalized: "Open",
    cycles: "1",
    efficacy: "0",
    externalBugTrackingSystem: null,
    historicTreatment: [
      {
        acceptanceDate: "",
        acceptanceStatus: "",
        assigned: "assigned-user-4",
        date: "2019-07-05 09:56:40",
        justification: "test progress justification",
        treatment: "IN PROGRESS",
        user: "usertreatment@test.test",
      },
    ],
    id: "af7a48b8-d8fc-41da-9282-d424fff563f0",
    lastReattackDate: moment()
      .subtract(numberOfDays, "days")
      .format("YYYY-MM-DD hh:mm:ss"),
    lastReattackRequester: "",
    lastRequestedReattackDate: undefined,
    remediated: false,
    reportDate: "",
    severity: "1",
    specific: "specific-3",
    stream: null,
    tag: "tag-7, tag-8",
    treatment: "IN PROGRESS",
    treatmentChanges: 1,
    treatmentDate: "2019-07-05 09:56:40",
    verification: "Verified",
    vulnerabilityType: "lines",
    where: "https://example.com/lines",
    zeroRisk: undefined,
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof AdditionalInfo).toStrictEqual("function");
  });

  it("should render in vulnerabilities", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();

    const wrapper: ReactWrapper = mount(
      <AdditionalInfo
        canDisplayHacker={false}
        onClose={jest.fn()}
        vulnerability={formatVulnerabilities([mockVuln])[0]}
      />
    );
    wrapper.update();

    expect(wrapper).toHaveLength(1);

    expect(wrapper.find(Label).first().find("span").text()).toBe(
      t("searchFindings.tabVuln.vulnTable.specificType.code")
    );

    wrapper.setProps({
      vulnerability: formatVulnerabilities([
        { ...mockVuln, vulnerabilityType: "inputs" },
      ])[0],
    });
    wrapper.update();

    expect(wrapper.find(Label).first().find("span").text()).toBe(
      t("searchFindings.tabVuln.vulnTable.specificType.app")
    );
  });
});
