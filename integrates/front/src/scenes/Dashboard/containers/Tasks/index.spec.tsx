import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { TasksContent } from "scenes/Dashboard/containers/Tasks";
import { AssignedVulnerabilitiesContext } from "scenes/Dashboard/context";
import {
  GET_ME_VULNERABILITIES_ASSIGNED,
  GET_USER_ORGANIZATIONS_GROUPS,
} from "scenes/Dashboard/queries";
import type {
  IGetMeVulnerabilitiesAssigned,
  IGetUserOrganizationsGroups,
} from "scenes/Dashboard/types";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgInfo } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgInfo").mockImplementation();

  return mockedNotifications;
});

describe("VulnerabilitiesView", (): void => {
  const mocksVulnerabilities: MockedResponse = {
    request: {
      query: GET_ME_VULNERABILITIES_ASSIGNED,
    },
    result: {
      data: {
        me: {
          vulnerabilitiesAssigned: [
            {
              __typename: "Vulnerability",
              currentState: "open",
              externalBugTrackingSystem: null,
              findingId: "422286126",
              groupName: "group1",
              id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
              lastTreatmentDate: "2019-07-05 09:56:40",
              lastVerificationDate: null,
              remediated: false,
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
              verification: null,
              vulnerabilityType: "inputs",
              where: "https://example.com/inputs",
              zeroRisk: null,
            },
            {
              __typename: "Vulnerability",
              currentState: "open",
              externalBugTrackingSystem: null,
              findingId: "422286126",
              groupName: "group2",
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
        },
      },
    },
  };

  const mocksUserGroups: MockedResponse = {
    request: {
      query: GET_USER_ORGANIZATIONS_GROUPS,
    },
    result: {
      data: {
        me: {
          organizations: [
            {
              groups: [
                {
                  name: "group1",
                  permissions: [
                    "api_mutations_request_vulnerabilities_verification_mutate",
                  ],
                  serviceAttributes: ["is_continuous"],
                },
                {
                  name: "group2",
                  permissions: [
                    "api_mutations_request_vulnerabilities_verification_mutate",
                  ],
                  serviceAttributes: [],
                },
              ],
              name: "orgtest",
            },
          ],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TasksContent).toStrictEqual("function");
  });

  it("should render container", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
    ]);

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/todos"]}>
        <AssignedVulnerabilitiesContext.Provider value={[[], jest.fn()]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/todos"}>
              <TasksContent
                meVulnerabilitiesAssigned={{
                  me: {
                    userEmail: "",
                    vulnerabilitiesAssigned: [],
                  },
                }}
                refetchVulnerabilitiesAssigned={jest.fn()}
                setUserRole={jest.fn()}
                userData={{
                  me: {
                    organizations: [{ groups: [], name: "orgtest" }],
                    userEmail: "",
                  },
                }}
              />
            </Route>
          </authzPermissionsContext.Provider>
        </AssignedVulnerabilitiesContext.Provider>
      </MemoryRouter>
    );

    wrapper.update();

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("tr").at(1).find("td").at(0).text()).toBe(
          "dataTableNext.noDataIndication"
        );
      });
    });
  });
});
