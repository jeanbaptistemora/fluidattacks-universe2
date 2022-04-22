import { PureAbility } from "@casl/ability";
import { render, screen, within } from "@testing-library/react";
import moment from "moment";
import React from "react";

import type { IVulnRowAttr } from "./types";

import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import { authzPermissionsContext } from "utils/authz/config";

describe("VulnComponent", (): void => {
  const numberOfDaysOldThanAWeek: number = 12;
  const numberOfDays: number = 5;
  const mockedPermissions: PureAbility<string> = new PureAbility([
    { action: "api_mutations_request_vulnerabilities_zero_risk_mutate" },
    { action: "api_mutations_update_vulnerability_treatment_mutate" },
    { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
  ]);
  const mocks: IVulnRowAttr[] = [
    {
      assigned: "",
      currentState: "open",
      currentStateCapitalized: "Open",
      externalBugTrackingSystem: null,
      findingId: "438679960",
      groupName: "test",
      historicTreatment: [
        {
          acceptanceDate: "",
          acceptanceStatus: "",
          assigned: "assigned-user-1",
          date: "2019-07-05 09:56:40",
          justification: "test progress justification",
          treatment: "IN PROGRESS",
          user: "usertreatment@test.test",
        },
      ],
      id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
      lastTreatmentDate: "2019-07-05 09:56:40",
      lastVerificationDate: null,
      remediated: true,
      reportDate: "",
      severity: "3",
      specific: "specific-1",
      stream: null,
      tag: "tag-1, tag-2",
      treatment: "",
      treatmentAcceptanceDate: "",
      treatmentAcceptanceStatus: "",
      treatmentAssigned: "assigned-user-1",
      treatmentDate: "2019-07-05 09:56:40",
      treatmentJustification: "test progress justification",
      treatmentUser: "usertreatment@test.test",
      verification: "Requested",
      vulnerabilityType: "inputs",
      where: "https://example.com/inputs",
      zeroRisk: "Requested",
    },
    {
      assigned: "",
      currentState: "closed",
      currentStateCapitalized: "Closed",
      externalBugTrackingSystem: null,
      findingId: "438679960",
      groupName: "test",
      historicTreatment: [
        {
          acceptanceDate: "",
          acceptanceStatus: "",
          assigned: "assigned-user-3",
          date: "2019-07-05 09:56:40",
          justification: "test progress justification",
          treatment: "IN PROGRESS",
          user: "usertreatment@test.test",
        },
      ],
      id: "a09c79fc-33fb-4abd-9f20-f3ab1f500bd0",
      lastTreatmentDate: "2019-07-05 09:56:40",
      lastVerificationDate: moment()
        .subtract(numberOfDays, "days")
        .format("YYYY-MM-DD hh:mm:ss"),
      remediated: false,
      reportDate: "",
      severity: "1",
      specific: "specific-2",
      stream: null,
      tag: "tag-5, tag-6",
      treatment: "",
      treatmentAcceptanceDate: "",
      treatmentAcceptanceStatus: "",
      treatmentAssigned: "assigned-user-3",
      treatmentDate: "2019-07-05 09:56:40",
      treatmentJustification: "test progress justification",
      treatmentUser: "usertreatment@test.test",
      verification: "Verified",
      vulnerabilityType: "lines",
      where: "https://example.com/lines",
      zeroRisk: null,
    },
    {
      assigned: "assigned-user-4",
      currentState: "open",
      currentStateCapitalized: "Open",
      externalBugTrackingSystem: null,
      findingId: "438679960",
      groupName: "test",
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
      lastTreatmentDate: "2019-07-05 09:56:40",
      lastVerificationDate: moment()
        .subtract(numberOfDaysOldThanAWeek, "days")
        .format("YYYY-MM-DD hh:mm:ss"),
      remediated: false,
      reportDate: "",
      severity: "1",
      specific: "specific-3",
      stream: null,
      tag: "tag-7, tag-8",
      treatment: "IN PROGRESS",
      treatmentAcceptanceDate: "",
      treatmentAcceptanceStatus: "",
      treatmentAssigned: "assigned-user-4",
      treatmentDate: "2019-07-05 09:56:40",
      treatmentJustification: "test progress justification",
      treatmentUser: "usertreatment@test.test",
      verification: "Verified",
      vulnerabilityType: "lines",
      where: "https://example.com/lines",
      zeroRisk: null,
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof VulnComponent).toBe("function");
  });

  it("should render in vulnerabilities", (): void => {
    expect.hasAssertions();

    const { rerender } = render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <VulnComponent
          canDisplayHacker={false}
          extraButtons={<div />}
          findingState={"open"}
          isEditing={true}
          isFindingReleased={true}
          isRequestingReattack={false}
          isVerifyingRequest={false}
          onVulnSelect={jest.fn()}
          vulnerabilities={mocks}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("table")).toBeInTheDocument();
    expect(
      within(screen.getAllByRole("row")[1]).getByRole("checkbox")
    ).not.toBeDisabled();
    expect(
      within(screen.getAllByRole("row")[2]).getByRole("checkbox")
    ).toBeDisabled();

    rerender(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <VulnComponent
          canDisplayHacker={false}
          extraButtons={<div />}
          findingState={"open"}
          isEditing={false}
          isFindingReleased={true}
          isRequestingReattack={true}
          isVerifyingRequest={false}
          onVulnSelect={jest.fn()}
          vulnerabilities={mocks}
        />
      </authzPermissionsContext.Provider>
    );

    expect(
      within(screen.getAllByRole("row")[1]).getByRole("checkbox")
    ).toBeDisabled();
    expect(
      within(screen.getAllByRole("row")[2]).getByRole("checkbox")
    ).toBeDisabled();
  });

  it("should render in vulnerabilities in draft", (): void => {
    expect.hasAssertions();

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <VulnComponent
          canDisplayHacker={false}
          extraButtons={<div />}
          findingState={"open"}
          isEditing={true}
          isFindingReleased={false}
          isRequestingReattack={false}
          isVerifyingRequest={false}
          onVulnSelect={jest.fn()}
          vulnerabilities={mocks}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("table")).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabDescription.editVuln")
    ).not.toBeInTheDocument();
    expect(screen.queryAllByRole("button")).toHaveLength(0);
    expect(screen.queryAllByRole("checkbox")).toHaveLength(0);
  });
});
