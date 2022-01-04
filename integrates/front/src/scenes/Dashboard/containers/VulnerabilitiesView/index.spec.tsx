import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { VulnsView } from "scenes/Dashboard/containers/VulnerabilitiesView";
import {
  GET_FINDING_AND_GROUP_INFO,
  GET_FINDING_VULNS,
} from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

describe("VulnerabilitiesView", (): void => {
  const mocksQueryFindingAndGroupInfo: MockedResponse = {
    request: {
      query: GET_FINDING_AND_GROUP_INFO,
      variables: {
        findingId: "422286126",
        groupName: "testgroup",
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
        group: {
          __typename: "Group",
          name: "testgroup",
          subscription: "continuous",
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

    expect(typeof VulnsView).toStrictEqual("function");
  });

  it("should render container", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate" },
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_resolvers_finding_zero_risk_resolve" },
    ]);

    const wrapper: ReactWrapper = mount(
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

    wrapper.update();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(
          wrapper.find("BootstrapTable").find("RowPureContent")
        ).toHaveLength(2);
      });
    });
  });

  it("should render container with additional permissions", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate" },
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_resolvers_finding_zero_risk_resolve" },
    ]);
    const wrapper: ReactWrapper = mount(
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

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);

        wrapper.find("Button#handleAcceptanceButton").simulate("click");

        expect(
          wrapper
            .find("div#vulnsToHandleAcceptance")
            .find("BootstrapTable")
            .find("RowPureContent")
        ).toHaveLength(1);
      });
    });
  });

  it("should render container and test request_button flow", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_mutations_request_vulnerabilities_verification_mutate" },
      { action: "api_resolvers_finding_zero_risk_resolve" },
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    const mockedServices: PureAbility<string> = new PureAbility([
      { action: "is_continuous" },
    ]);
    const wrapper: ReactWrapper = mount(
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

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
        const totalButtons = 3;

        expect(wrapper).toHaveLength(1);

        expect(wrapper.find("Button")).toHaveLength(totalButtons);
      });
    });

    const tableVulns: ReactWrapper = wrapper
      .find({ id: "vulnerabilitiesTable" })
      .at(0);
    const selectionCell: ReactWrapper = tableVulns.find("SelectionCell");
    selectionCell.last().simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();
        const buttons: ReactWrapper = wrapper.find("Button");
        const requestButton: ReactWrapper = buttons.filterWhere(
          (button: ReactWrapper): boolean =>
            button
              .text()
              .includes(t("searchFindings.tabDescription.requestVerify.tex"))
        );

        expect(requestButton).toHaveLength(1);
        expect(wrapper.find("UpdateVerificationModal")).toHaveLength(0);

        requestButton.simulate("click");
        wrapper.update();

        expect(
          wrapper
            .find("Button")
            .filterWhere((button: ReactWrapper): boolean =>
              button.text().includes(t("searchFindings.tabVuln.buttons.edit"))
            )
        ).toHaveLength(0);
        expect(wrapper.find("UpdateVerificationModal")).toHaveLength(1);
      });
    });
  });

  it("should render container and test verify_button flow", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_resolvers_finding_zero_risk_resolve" },
      { action: "api_mutations_verify_vulnerabilities_request_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
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

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);

        expect(wrapper.find("Button")).toHaveLength(2);
      });
    });

    const buttons: ReactWrapper = wrapper.find("Button");
    const verifyButton: ReactWrapper = buttons.filterWhere(
      (button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("searchFindings.tabDescription.markVerified.text"))
    );

    wrapper.update();

    expect(verifyButton).toHaveLength(1);
    expect(
      wrapper
        .find({ id: "vulnerabilitiesTable" })
        .at(0)
        .find("input[disabled=false]")
    ).toHaveLength(2);

    verifyButton.simulate("click");

    expect(
      wrapper
        .find("Button")
        .filterWhere((button: ReactWrapper): boolean =>
          button.text().includes(t("searchFindings.tabVuln.buttons.edit"))
        )
    ).toHaveLength(0);
    expect(
      wrapper
        .find({ id: "vulnerabilitiesTable" })
        .at(0)
        .find("input[disabled=false]")
    ).toHaveLength(1);
    expect(wrapper.find("UpdateVerificationModal")).toHaveLength(0);

    const tableVulns: ReactWrapper = wrapper
      .find({ id: "vulnerabilitiesTable" })
      .at(0);
    const selectionCell: ReactWrapper = tableVulns.find("SelectionCell");
    selectionCell.first().simulate("click");
    wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("searchFindings.tabDescription.markVerified.text"))
      )
      .first()
      .simulate("click");
    wrapper.update();

    expect(wrapper.find("UpdateVerificationModal")).toHaveLength(1);
  });
});
