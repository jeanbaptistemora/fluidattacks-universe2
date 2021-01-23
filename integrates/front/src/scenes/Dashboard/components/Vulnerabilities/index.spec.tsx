import type { IVulnRowAttr } from "./types";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import { act } from "react-dom/test-utils";
import moment from "moment";
import { mount } from "enzyme";

describe("VulnComponent", (): void => {
  const numberOfDaysOldThanAWeek: number = 12;
  const numberOfDays: number = 5;
  const mocks: IVulnRowAttr[] = [
    {
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
          treatmentManager: "treatment-manager-1",
          user: "usertreatment@test.test",
        },
      ],
      id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
      lastReattackDate: "",
      lastReattackRequester: "testrequester@test.com",
      lastRequestedReattackDate: "",
      remediated: true,
      reportDate: "",
      severity: "3",
      specific: "specific-1",
      tag: "tag-1, tag-2",
      treatment: "",
      treatmentChanges: 1,
      treatmentDate: "",
      treatmentManager: "",
      verification: "Requested",
      vulnType: "inputs",
      where: "https://example.com/inputs",
      zeroRisk: "Requested",
    },
    {
      currentState: "closed",
      currentStateCapitalized: "Closed",
      cycles: "1",
      efficacy: "100",
      externalBts: "",
      historicTreatment: [
        {
          acceptanceDate: "",
          acceptanceStatus: "",
          date: "2019-07-05 09:56:40",
          justification: "test progress justification",
          treatment: "IN PROGRESS",
          treatmentManager: "treatment-manager-3",
          user: "usertreatment@test.test",
        },
      ],
      id: "a09c79fc-33fb-4abd-9f20-f3ab1f500bd0",
      lastReattackDate: moment()
        .subtract(numberOfDays, "days")
        .format("YYYY-MM-DD hh:mm:ss"),
      lastReattackRequester: "",
      lastRequestedReattackDate: "",
      remediated: false,
      reportDate: "",
      severity: "1",
      specific: "specific-2",
      tag: "tag-5, tag-6",
      treatment: "",
      treatmentChanges: 1,
      treatmentDate: "",
      treatmentManager: "",
      verification: "Verified",
      vulnType: "lines",
      where: "https://example.com/lines",
      zeroRisk: "",
    },
    {
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
        .subtract(numberOfDaysOldThanAWeek, "days")
        .format("YYYY-MM-DD hh:mm:ss"),
      lastReattackRequester: "",
      lastRequestedReattackDate: "",
      remediated: false,
      reportDate: "",
      severity: "1",
      specific: "specific-3",
      tag: "tag-7, tag-8",
      treatment: "IN PROGRESS",
      treatmentChanges: 1,
      treatmentDate: "2019-07-05 09:56:40",
      treatmentManager: "treatment-manager-4",
      verification: "Verified",
      vulnType: "lines",
      where: "https://example.com/lines",
      zeroRisk: "",
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof VulnComponent).toStrictEqual("function");
  });

  it("should render in vulnerabilities", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <VulnComponent
        canDisplayAnalyst={false}
        findingId={"480857698"}
        groupName={"test"}
        isEditing={true}
        isRequestingReattack={false}
        isVerifyingRequest={false}
        onVulnSelect={jest.fn()}
        vulnerabilities={mocks}
      />
    );
    wrapper.update();

    expect(wrapper).toHaveLength(1);

    const tableVulns: ReactWrapper = wrapper
      .find({ id: "vulnerabilitiesTable" })
      .at(0);
    const selectionCell: ReactWrapper = tableVulns.find("SelectionCell");

    expect(selectionCell.at(0).find("input").prop("disabled")).toBe(false);
    expect(selectionCell.at(1).find("input").prop("disabled")).toBe(true);

    act((): void => {
      wrapper.setProps({ isEditing: false, isRequestingReattack: true });
      wrapper.update();
    });

    const tableVulnsUpdated: ReactWrapper = wrapper
      .find({ id: "vulnerabilitiesTable" })
      .at(0);
    const selectionCellUpdated: ReactWrapper = tableVulnsUpdated.find(
      "SelectionCell"
    );

    expect(selectionCellUpdated.at(0).find("input").prop("disabled")).toBe(
      true
    );
    expect(selectionCellUpdated.at(1).find("input").prop("disabled")).toBe(
      true
    );
  });
});
