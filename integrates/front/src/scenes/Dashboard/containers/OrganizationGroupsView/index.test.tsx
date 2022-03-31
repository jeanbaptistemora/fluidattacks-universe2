import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import {
  ADD_GROUP_MUTATION,
  GROUPS_NAME_QUERY,
} from "scenes/Dashboard/components/AddGroupModal/queries";
import { OrganizationGroups } from "scenes/Dashboard/containers/OrganizationGroupsView";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/OrganizationGroupsView/queries";
import type { IOrganizationGroupsProps } from "scenes/Dashboard/containers/OrganizationGroupsView/types";
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

describe("Organization groups view", (): void => {
  const mockProps: IOrganizationGroupsProps = {
    organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationGroups).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              groups: [
                {
                  description: "Continuous type test group",
                  events: [],
                  hasMachine: true,
                  hasSquad: true,
                  name: "unittesting",
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "user",
                },
                {
                  description: "One-shot type test group",
                  events: [],
                  hasMachine: true,
                  hasSquad: true,
                  name: "oneshottest",
                  service: "WHITE",
                  subscription: "oneshot",
                  userRole: "user_manager",
                },
                {
                  description: "Continuous group for deletion",
                  events: [],
                  hasMachine: true,
                  hasSquad: false,
                  name: "pendingGroup",
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "customer_manager",
                },
              ],
              name: "okada",
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_group_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/groups"}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <OrganizationGroups organizationId={mockProps.organizationId} />
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });

    expect(screen.getAllByRole("row")).toHaveLength(4);

    const UNIT_TESTING_ROW_AT = 3;

    expect(screen.getAllByRole("button")[0].textContent).toMatch(
      /organization.tabs.groups.newGroup.new.text/u
    );
    expect(screen.getAllByRole("row")[1].textContent).toContain("Oneshottest");
    expect(screen.getAllByRole("row")[1].textContent).toContain("Oneshot");
    expect(screen.getAllByRole("row")[1].textContent).toContain(
      "userModal.roles.userManager"
    );

    expect(screen.getAllByRole("row")[2].textContent).toContain("Pendinggroup");
    expect(screen.getAllByRole("row")[2].textContent).toContain("Machine");
    expect(screen.getAllByRole("row")[2].textContent).toContain(
      "userModal.roles.customerManager"
    );

    expect(
      screen.getAllByRole("row")[UNIT_TESTING_ROW_AT].textContent
    ).toContain("Unittesting");
    expect(
      screen.getAllByRole("row")[UNIT_TESTING_ROW_AT].textContent
    ).toContain("Squad");
    expect(
      screen.getAllByRole("row")[UNIT_TESTING_ROW_AT].textContent
    ).toContain("userModal.roles.user");

    userEvent.click(screen.getByRole("cell", { name: "Unittesting" }));
  });

  it("should show an error", async (): Promise<void> => {
    expect.hasAssertions();

    const mockErrors: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <MockedProvider addTypename={false} mocks={mockErrors}>
          <Route path={"/orgs/:organizationName/groups"}>
            <OrganizationGroups organizationId={mockProps.organizationId} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    expect(screen.queryAllByRole("table")).toHaveLength(0);

    jest.clearAllMocks();
  });

  it("should add a new group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              groups: [
                {
                  description: "Continuous type test group",
                  events: [],
                  hasMachine: true,
                  hasSquad: true,
                  name: "unittesting",
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "user",
                },
                {
                  description: "One-shot type test group",
                  events: [],
                  hasMachine: true,
                  hasSquad: true,
                  name: "oneshottest",
                  service: "WHITE",
                  subscription: "oneshot",
                  userRole: "user_manager",
                },
              ],
              name: "okada",
            },
          },
        },
      },
      {
        request: {
          query: GROUPS_NAME_QUERY,
        },
        result: {
          data: {
            internalNames: {
              name: "AKAME",
            },
          },
        },
      },
      {
        request: {
          query: ADD_GROUP_MUTATION,
          variables: {
            description: "Test group",
            groupName: "AKAME",
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            organization: "OKADA",
            service: "WHITE",
            subscription: "CONTINUOUS",
          },
        },
        result: {
          data: {
            addGroup: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              groups: [
                {
                  description: "Continuous type test group",
                  events: [],
                  hasAsm: true,
                  hasForces: true,
                  hasMachine: true,
                  hasSquad: true,
                  name: "unittesting",
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "user",
                },
                {
                  description: "One-shot type test group",
                  events: [],
                  hasAsm: true,
                  hasForces: false,
                  hasMachine: true,
                  hasSquad: true,
                  name: "oneshottest",
                  service: "WHITE",
                  subscription: "oneshot",
                  userRole: "user_manager",
                },
                {
                  description: "Test group",
                  events: [],
                  hasAsm: true,
                  hasForces: true,
                  hasMachine: true,
                  hasSquad: true,
                  name: "akame",
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "user_manager",
                },
              ],
              name: "okada",
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_group_mutate" },
    ]);

    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/groups"}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <OrganizationGroups organizationId={mockProps.organizationId} />
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    const numberOfRows = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });

    expect(screen.getAllByRole("row")).toHaveLength(numberOfRows);

    userEvent.click(
      screen.getByText("organization.tabs.groups.newGroup.new.text")
    );

    await waitFor((): void => {
      expect(
        screen.getByText("organization.tabs.groups.newGroup.new.group")
      ).toBeInTheDocument();
    });

    expect(screen.getByText("confirmmodal.proceed")).toBeDisabled();

    userEvent.type(
      screen.getByRole("textbox", { name: "description" }),
      "Test group"
    );
    await waitFor((): void => {
      expect(screen.getByDisplayValue("AKAME")).toBeInTheDocument();
    });
    userEvent.selectOptions(screen.getByRole("combobox", { name: "type" }), [
      "CONTINUOUS",
    ]);

    await waitFor((): void => {
      expect(screen.getByText("confirmmodal.proceed")).not.toBeDisabled();
    });

    userEvent.click(screen.getByText("confirmmodal.proceed"));

    await waitFor(
      (): void => {
        expect(screen.queryAllByRole("row")).toHaveLength(4);
      },
      { timeout: 2000 }
    );

    expect(msgSuccess).toHaveBeenCalledWith(
      "organization.tabs.groups.newGroup.success",
      "organization.tabs.groups.newGroup.titleSuccess"
    );

    jest.clearAllMocks();
  });
});
