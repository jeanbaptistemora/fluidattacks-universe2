import type { IVulnRowAttr } from "./types";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities/newIndex";
import { act } from "react-dom/test-utils";
import { mount } from "enzyme";

describe("VulnComponent", (): void => {
  const mocks: IVulnRowAttr[] = [
    {
      currentState: "open",
      currentStateCapitalized: "Open",
      cycles: "",
      efficacy: "",
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
      lastRequestedReattackDate: "",
      remediated: true,
      reportDate: "",
      severity: "3",
      specific: "specific-1",
      tag: "tag-1, tag-2",
      treatment: "",
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
      cycles: "",
      efficacy: "",
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
      lastRequestedReattackDate: "",
      remediated: false,
      reportDate: "",
      severity: "1",
      specific: "specific-2",
      tag: "tag-5, tag-6",
      treatment: "",
      treatmentDate: "",
      treatmentManager: "",
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
        findingId={"480857698"}
        groupName={"test"}
        isConfirmingZeroRisk={false}
        isEditing={true}
        isRejectingZeroRisk={false}
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
    const tableSpecifics: ReactWrapper = tableVulns.find({ columnIndex: 2 });
    const selectionCell: ReactWrapper = tableVulns.find("SelectionCell");

    expect(tableSpecifics.at(0).text()).toStrictEqual("specific-1");
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
