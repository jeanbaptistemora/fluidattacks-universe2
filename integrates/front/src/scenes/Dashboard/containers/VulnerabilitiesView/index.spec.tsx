import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { Provider } from "react-redux";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { VulnsView } from "scenes/Dashboard/containers/VulnerabilitiesView";
import { act } from "react-dom/test-utils";
import { authzPermissionsContext } from "utils/authz/config";
import { mount } from "enzyme";
import store from "store";
import waitForExpect from "wait-for-expect";
import { MemoryRouter, Route } from "react-router-dom";

describe("VulnerabilitiesView", (): void => {
  const mocksQuery: MockedResponse = {
    request: {
      query: GET_FINDING_VULN_INFO,
      variables: {
        canRetrieveAnalyst: true,
        findingId: "422286126",
        groupName: "testgroup",
      },
    },
    result: {
      data: {
        finding: {
          id: "422286126",
          newRemediated: true,
          state: "open",
          verified: false,
          vulnerabilities: [
            {
              analyst: "useranalyst@test.test",
              currentState: "open",
              cycles: "",
              efficacy: "",
              externalBts: "",
              findingId: "422286126",
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
              lastRequestedReattackDate: "2019-10-05 09:56:40",
              remediated: true,
              reportDate: "2019-07-05 09:56:40",
              severity: "",
              specific: "specific-1",
              tag: "tag-1, tag-2",
              treatmentDate: "2019-07-05 09:56:40",
              verification: "Requested",
              vulnType: "inputs",
              where: "https://example.com/inputs",
              zeroRisk: "Requested",
            },
            {
              analyst: "useranalyst@test.test",
              currentState: "closed",
              cycles: "",
              efficacy: "",
              externalBts: "",
              findingId: "422286126",
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
              lastReattackDate: "",
              lastReattackRequester: "",
              lastRequestedReattackDate: "",
              remediated: false,
              reportDate: "2019-07-05 09:56:40",
              severity: "",
              specific: "specific-2",
              tag: "tag-3",
              treatmentDate: "2019-07-05 09:56:40",
              verification: "Verified",
              vulnType: "lines",
              where: "https://example.com/lines",
              zeroRisk: "",
            },
          ],
        },
        project: {
          subscription: "continuous",
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

    const wrapper: ReactWrapper = mount(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={[mocksQuery]}>
            <authzPermissionsContext.Provider
              value={
                new PureAbility([
                  {
                    action:
                      "backend_api_resolvers_vulnerability_analyst_resolve",
                  },
                ])
              }
            >
              <Route
                component={VulnsView}
                path={
                  "/orgs/:organizationName/groups/:projectName/vulns/:findingId/locations"
                }
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
          expect(
            wrapper.find("BootstrapTable").find("RowPureContent")
          ).toHaveLength(1);
        });
      }
    );
  });

  it("should render container with additional permissions", async (): Promise<
    void
  > => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_confirm_zero_risk_vuln_mutate" },
      { action: "backend_api_resolvers_vulnerability_analyst_resolve" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={[mocksQuery]}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={VulnsView}
                path={
                  "/orgs/:organizationName/groups/:projectName/vulns/:findingId/locations"
                }
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
          expect(
            wrapper.find("BootstrapTable").find("RowPureContent")
          ).toHaveLength(2);
        });
      }
    );
  });
});
