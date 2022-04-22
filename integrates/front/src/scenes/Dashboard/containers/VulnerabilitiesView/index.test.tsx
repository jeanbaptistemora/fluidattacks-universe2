import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { VulnsView } from "scenes/Dashboard/containers/VulnerabilitiesView";
import {
  GET_FINDING_AND_GROUP_INFO,
  GET_FINDING_VULNS,
} from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

describe("VulnerabilitiesView", (): void => {
  const totalButtons = 3;
  const mocksQueryFindingAndGroupInfo: MockedResponse = {
    request: {
      query: GET_FINDING_AND_GROUP_INFO,
      variables: {
        findingId: "422286126",
      },
    },
    result: {
      data: {
        finding: {
          __typename: "Finding",
          id: "422286126",
          releaseDate: "2019-07-05 08:56:40",
          remediated: false,
          state: "open",
          verified: false,
        },
      },
    },
  };

  const mocksQueryFindingVulns: MockedResponse = {
    request: {
      query: GET_FINDING_VULNS,
      variables: {
        canRetrieveZeroRisk: true,
        findingId: "422286126",
      },
    },
    result: {
      data: {
        finding: {
          __typename: "Finding",
          vulnerabilities: [
            {
              __typename: "Vulnerability",
              currentState: "open",
              externalBugTrackingSystem: null,
              findingId: "422286126",
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
              reportDate: "2019-07-05 09:56:40",
              severity: "",
              specific: "specific-1",
              stream: "home > blog > articulo",
              tag: "tag-1, tag-2",
              treatment: "IN_PROGRESS",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-1",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              treatmentUser: "usertreatment@test.test",
              verification: "Requested",
              vulnerabilityType: "inputs",
              where: "https://example.com/inputs",
              zeroRisk: null,
            },
            {
              __typename: "Vulnerability",
              currentState: "open",
              externalBugTrackingSystem: null,
              findingId: "422286126",
              historicTreatment: [
                {
                  acceptanceDate: "",
                  acceptanceStatus: "",
                  assigned: "assigned-user-4@test.test",
                  date: "2020-07-05 09:56:40",
                  justification: "test progress justification",
                  treatment: "IN PROGRESS",
                  user: "usertreatment4@test.test",
                },
              ],
              id: "6903f3e4-a8ee-4a5d-ac38-fb738ec7e540",
              lastTreatmentDate: "2019-07-05 09:56:40",
              lastVerificationDate: null,
              remediated: false,
              reportDate: "2020-07-05 09:56:40",
              severity: "",
              specific: "specific-3",
              stream: null,
              tag: "tag-3",
              treatment: "IN_PROGRESS",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-1",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              treatmentUser: "usertreatment@test.test",
              verification: null,
              vulnerabilityType: "lines",
              where: "https://example.com/tests",
              zeroRisk: null,
            },
          ],
          zeroRisk: [
            {
              __typename: "Vulnerability",
              currentState: "open",
              externalBugTrackingSystem: null,
              findingId: "422286126",
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
              lastVerificationDate: null,
              remediated: false,
              reportDate: "2019-07-05 09:56:40",
              severity: "",
              specific: "specific-2",
              stream: null,
              tag: "tag-3",
              treatment: "IN_PROGRESS",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-1",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              treatmentUser: "usertreatment@test.test",
              verification: "Verified",
              vulnerabilityType: "lines",
              where: "https://example.com/lines",
              zeroRisk: "Requested",
            },
          ],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof VulnsView).toBe("function");
  });

  it("should render container", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate" },
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_resolvers_finding_zero_risk_resolve" },
    ]);

    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <MockedProvider
          addTypename={true}
          mocks={[mocksQueryFindingAndGroupInfo, mocksQueryFindingVulns]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={VulnsView}
              path={
                "/orgs/:organizationName/groups/:groupName/vulns/:findingId/locations"
              }
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(totalButtons);
    });
  });

  it("should render container with additional permissions", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate" },
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_resolvers_finding_zero_risk_resolve" },
    ]);
    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <MockedProvider
          addTypename={true}
          mocks={[mocksQueryFindingAndGroupInfo, mocksQueryFindingVulns]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={VulnsView}
              path={
                "/orgs/:organizationName/groups/:groupName/vulns/:findingId/locations"
              }
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(2);
    });

    expect(
      screen.queryByRole("combobox", { name: "treatment" })
    ).not.toBeInTheDocument();

    userEvent.click(
      screen.getByRole("button", {
        name: "searchFindings.tabVuln.buttons.handleAcceptance",
      })
    );
    await waitFor((): void => {
      expect(
        screen.queryByText(
          "searchFindings.tabDescription.handleAcceptanceModal.title"
        )
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByRole("combobox", { name: "treatment" })
    ).toBeInTheDocument();
  });

  it("should render container and test request_button flow", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_mutations_request_vulnerabilities_verification_mutate" },
      { action: "api_resolvers_finding_zero_risk_resolve" },
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    const mockedServices: PureAbility<string> = new PureAbility([
      { action: "is_continuous" },
    ]);
    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <MockedProvider
          addTypename={true}
          mocks={[mocksQueryFindingAndGroupInfo, mocksQueryFindingVulns]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider value={mockedServices}>
              <Route
                component={VulnsView}
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId/locations"
                }
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(totalButtons);
    });
    userEvent.click(screen.queryAllByRole("checkbox")[2]);

    expect(
      screen.queryByText(
        "searchFindings.tabDescription.remediationModal.titleRequest"
      )
    ).not.toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).toBeInTheDocument();

    userEvent.click(
      screen.getByText("searchFindings.tabDescription.requestVerify.text")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText(
          "searchFindings.tabDescription.remediationModal.titleRequest"
        )
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).not.toBeInTheDocument();
  });

  it("should render container and test verify_button flow", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_resolvers_finding_zero_risk_resolve" },
      { action: "api_mutations_verify_vulnerabilities_request_mutate" },
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <MockedProvider
          addTypename={true}
          mocks={[mocksQueryFindingAndGroupInfo, mocksQueryFindingVulns]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={VulnsView}
              path={
                "/orgs/:organizationName/groups/:groupName/vulns/:findingId/locations"
              }
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(totalButtons);
    });

    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).toBeInTheDocument();
    expect(screen.queryAllByRole("checkbox")[2]).not.toBeDisabled();
    expect(
      screen.queryByText(
        "searchFindings.tabDescription.remediationModal.titleObservations"
      )
    ).not.toBeInTheDocument();

    userEvent.click(
      screen.getByText("searchFindings.tabDescription.markVerified.text")
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox")[2]).toBeDisabled();
    });

    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).not.toBeInTheDocument();
    expect(screen.queryAllByRole("checkbox")[1]).not.toBeDisabled();

    userEvent.click(screen.queryAllByRole("checkbox")[1]);
    userEvent.click(
      screen.getByText("searchFindings.tabDescription.markVerified.text")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText(
          "searchFindings.tabDescription.remediationModal.titleObservations"
        )
      ).toBeInTheDocument();
    });
  });
});
