import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import moment from "moment";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IVulnRowAttr } from "../types";
import { TreatmentTracking } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/index";
import { formatVulnerabilities } from "scenes/Dashboard/components/Vulnerabilities/utils";

describe("TrackingTreatment", (): void => {
  const numberOfDays: number = 5;
  const mockVuln: IVulnRowAttr = {
    commitHash: "",
    currentState: "open",
    currentStateCapitalized: "Open",
    cycles: "1",
    efficacy: "0",
    externalBugTrackingSystem: "",
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
    vulnerabilityType: "lines",
    where: "https://example.com/lines",
    zeroRisk: "",
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TreatmentTracking).toStrictEqual("function");
  });

  it("should render in treatment tracking", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const onClose: jest.Mock = jest.fn();

    const wrapper: ReactWrapper = mount(
      <TreatmentTracking
        historicTreatment={
          formatVulnerabilities([mockVuln])[0].historicTreatment
        }
        onClose={onClose}
      />
    );
    wrapper.update();

    expect(wrapper).toHaveLength(1);

    expect(wrapper.find("li").first().find("p").first().text()).toBe(
      t("searchFindings.tabDescription.treatment.inProgress")
    );

    const closeButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains(t("searchFindings.tabVuln.close").toString())
      )
      .first();

    closeButton.simulate("click");
    wrapper.update();

    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
