import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { TasksContent } from "scenes/Dashboard/containers/Tasks";
import {
  GET_ME_VULNERABILITIES_ASSIGNED,
  GET_USER_ORGANIZATIONS_GROUPS,
} from "scenes/Dashboard/queries";
import type {
  IGetMeVulnerabilitiesAssigned,
  IGetUserOrganizationsGroups,
} from "scenes/Dashboard/types";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

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
              treatment: "ACCEPTED",
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
                    "api_mutations_update_vulnerabilities_treatment_mutate",
                    "api_resolvers_group_stakeholders_resolve",
                  ],
                  serviceAttributes: ["is_continuous"],
                },
                {
                  name: "group2",
                  permissions: [
                    "api_mutations_request_vulnerabilities_verification_mutate",
                    "api_mutations_update_vulnerabilities_treatment_mutate",
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

  it("should handle reattack button basic", async (): Promise<void> => {
    expect.hasAssertions();

    const refreshClick: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
    ]);

    const { container } = render(
      <MemoryRouter initialEntries={["/todos"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Route path={"/todos"}>
            <TasksContent
              meVulnerabilitiesAssigned={
                (
                  mocksVulnerabilities.result as Dictionary<{
                    me: IGetMeVulnerabilitiesAssigned["me"];
                  }>
                ).data
              }
              refetchVulnerabilitiesAssigned={jest.fn()}
              setUserRole={refreshClick}
              userData={
                (
                  mocksUserGroups.result as Dictionary<{
                    me: IGetUserOrganizationsGroups["me"];
                  }>
                ).data
              }
            />
          </Route>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    userEvent.click(container.querySelector("#refresh-assigned") as Element);

    await waitFor((): void => {
      expect(refreshClick).toHaveBeenCalledTimes(1);
    });

    expect(screen.getAllByRole("checkbox")[1]).not.toBeChecked();

    userEvent.click(screen.getAllByRole("checkbox")[1]);
    userEvent.click(screen.getAllByRole("checkbox")[2]);

    expect(screen.getAllByRole("checkbox")[1]).toBeChecked();

    await waitFor((): void => {
      expect(
        screen.getByText("searchFindings.tabDescription.requestVerify.text")
      ).not.toBeDisabled();
    });

    userEvent.click(
      screen.getByText("searchFindings.tabDescription.requestVerify.text")
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.tabVuln.info.text",
        "searchFindings.tabVuln.info.title"
      );
    });

    expect(msgError).toHaveBeenCalledWith(
      "searchFindings.tabVuln.errors.selectedVulnerabilities"
    );
  });

  it("should handle edit button basic", async (): Promise<void> => {
    expect.hasAssertions();

    const refreshClick: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
    ]);

    render(
      <MemoryRouter initialEntries={["/todos"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider addTypename={false} mocks={[]}>
            <Route path={"/todos"}>
              <TasksContent
                meVulnerabilitiesAssigned={
                  (
                    mocksVulnerabilities.result as Dictionary<{
                      me: IGetMeVulnerabilitiesAssigned["me"];
                    }>
                  ).data
                }
                refetchVulnerabilitiesAssigned={jest.fn()}
                setUserRole={refreshClick}
                userData={
                  (
                    mocksUserGroups.result as Dictionary<{
                      me: IGetUserOrganizationsGroups["me"];
                    }>
                  ).data
                }
              />
            </Route>
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    userEvent.click(screen.getAllByRole("checkbox")[1]);
    userEvent.click(screen.getAllByRole("checkbox")[2]);

    await waitFor((): void => {
      expect(screen.getAllByRole("checkbox")[2]).toBeChecked();
    });

    userEvent.click(screen.getByText("searchFindings.tabVuln.buttons.edit"));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabDescription.editVuln")
      ).toBeInTheDocument();
    });

    expect(screen.getByRole("combobox", { name: "treatment" })).toHaveValue(
      "ACCEPTED"
    );

    userEvent.click(screen.getByText("group.findings.report.modalClose"));

    await waitFor((): void => {
      expect(screen.getByRole("combobox", { name: "treatment" })).toHaveValue(
        "IN_PROGRESS"
      );
    });

    userEvent.click(screen.getByText("group.findings.report.modalClose"));

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabDescription.editVuln")
      ).not.toBeInTheDocument();
    });
  });
});
