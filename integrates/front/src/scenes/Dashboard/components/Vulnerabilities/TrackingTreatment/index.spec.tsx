import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import moment from "moment";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IVulnRowAttr } from "../types";
import { TreatmentTracking } from "scenes/Dashboard/components/Vulnerabilities/TrackingTreatment/index";
import { formatVulnerabilities } from "scenes/Dashboard/components/Vulnerabilities/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { formatDropdownField } from "utils/formatHelpers";

describe("TrackingTreatment", (): void => {
  const numberOfDays: number = 5;
  const historicTreatment: IHistoricTreatment[] = [
    {
      date: "2019-01-17 10:06:04",
      treatment: "NEW",
      user: "",
    },
    {
      acceptanceStatus: "SUBMITTED",
      assigned: "usermanager1@test.test",
      date: "2020-02-17 18:36:24",
      justification: "Some of the resources",
      treatment: "ACCEPTED_UNDEFINED",
      user: "usertreatment1@test.test",
    },
    {
      acceptanceStatus: "APPROVED",
      assigned: "usermanager2@test.test",
      date: "2020-02-18 18:36:24",
      justification: "The headers must be",
      treatment: "ACCEPTED_UNDEFINED",
      user: "usertreatment2@test.test",
    },
    {
      acceptanceDate: "2020-10-09 15:29:48",
      assigned: "usermanager3@test.test",
      date: "2020-10-02 15:29:48",
      justification: "The headers must be",
      treatment: "ACCEPTED",
      user: "usertreatment3@test.test",
    },
    {
      assigned: "usermanager4@test.test",
      date: "2020-10-08 15:29:48",
      justification: "The headers must be",
      treatment: "IN PROGRESS",
      user: "usertreatment4@test.test",
    },
  ];
  const mockVuln1: IVulnRowAttr = {
    assigned: "assigned-treatment-4",
    commitHash: undefined,
    currentState: "open",
    currentStateCapitalized: "Open",
    cycles: "1",
    efficacy: "0",
    externalBugTrackingSystem: undefined,
    historicTreatment: [...historicTreatment],
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
    stream: undefined,
    tag: "tag-7, tag-8",
    treatment: "IN PROGRESS",
    treatmentChanges: 1,
    treatmentDate: "2019-07-05 09:56:40",
    verification: "Verified",
    vulnerabilityType: "lines",
    where: "https://example.com/lines",
    zeroRisk: "",
  };

  const mockVuln2: IVulnRowAttr = {
    ...mockVuln1,
    historicTreatment: [...historicTreatment.slice(0, 2)],
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
          formatVulnerabilities([mockVuln1])[0].historicTreatment
        }
        onClose={onClose}
      />
    );
    wrapper.update();

    expect(wrapper).toHaveLength(1);

    const newNumberOfFields: number = 1;
    const normalNumberOfFields: number = 3;
    const permanentlyNumberOfFields: number = 5;

    expect(wrapper.find("li").first().find("p")).toHaveLength(
      normalNumberOfFields
    );
    expect(wrapper.find("li").at(1).find("p")).toHaveLength(
      normalNumberOfFields
    );
    expect(wrapper.find("li").at(2).find("p")).toHaveLength(
      permanentlyNumberOfFields
    );
    expect(wrapper.find("li").last().find("p")).toHaveLength(newNumberOfFields);
    expect(wrapper.find("li").first().find("p").first().text()).toBe(
      t("searchFindings.tabDescription.treatment.inProgress")
    );

    wrapper.setProps({
      historicTreatment: formatVulnerabilities([mockVuln2])[0]
        .historicTreatment,
    });
    wrapper.update();

    expect(wrapper.find("li").first().find("p")).toHaveLength(
      normalNumberOfFields
    );
    expect(wrapper.find("li").first().find("p").first().text()).toBe(
      t(
        formatDropdownField(
          formatVulnerabilities([mockVuln2])[0].historicTreatment.slice(-1)[0]
            .treatment
        )
      ) + t("searchFindings.tabDescription.treatment.pendingApproval")
    );

    const rejectedObservation: string = "The treatment was rejected";

    wrapper.setProps({
      historicTreatment: [
        ...formatVulnerabilities([mockVuln2])[0].historicTreatment,
        {
          acceptanceStatus: "REJECTED",
          assigned: "usermanager2@test.test",
          date: "2020-02-18 18:36:24",
          justification: rejectedObservation,
          treatment: "ACCEPTED_UNDEFINED",
          user: "usertreatment2@test.test",
        },
        {
          date: "2020-02-18 18:36:25",
          treatment: "NEW",
          user: "",
        },
      ],
    });
    wrapper.update();

    expect(wrapper.find("li").first().find("p")).toHaveLength(
      newNumberOfFields
    );
    expect(wrapper.find("li").at(1).find("p")).toHaveLength(
      normalNumberOfFields
    );
    expect(wrapper.find("li").at(1).find("p").first().text()).toBe(
      t(
        formatDropdownField(
          formatVulnerabilities([mockVuln2])[0].historicTreatment.slice(-1)[0]
            .treatment
        )
      ) + t("searchFindings.tabDescription.treatment.pendingApproval")
    );
    expect(wrapper.find("li").at(1).find("p").last().text()).toBe(
      `${t(
        "searchFindings.tabTracking.justification"
      )}\u00a0${rejectedObservation}`
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
