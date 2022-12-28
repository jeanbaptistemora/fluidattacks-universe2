import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupContent } from ".";
import { GET_GROUP_DATA } from "../containers/Group-Content/GroupScopeView/GroupSettingsView/queries";
import type { IGroupData } from "../containers/Group-Content/GroupScopeView/GroupSettingsView/Services/types";
import type { IGetOrganizationId } from "../containers/Organization-Content/OrganizationNav/types";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

describe("groupContent", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupContent).toBe("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_ID,
          variables: {
            organizationName: "testorg",
          },
        },
        result: {
          data: {
            organizationId: {
              id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
              name: "testorg",
            },
          },
        },
      },
    ];
    const numberOfLinks: number = 5;
    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/test/vulns"]}>
        <MockedProvider addTypename={false} mocks={mockedQueries}>
          <authzPermissionsContext.Provider value={new PureAbility([])}>
            <Route
              component={GroupContent}
              path={"/orgs/:organizationName/groups/:groupName/vulns"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("link")).toHaveLength(numberOfLinks);
    });
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_ID,
          variables: {
            organizationName: "testorg",
          },
        },
        result: {
          data: {
            organizationId: {
              id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
              name: "testorg",
            },
          },
        },
      },
    ];
    const numberOfLinksWithPermissions: number = 8;
    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_group_consulting_resolve" },
      { action: "api_resolvers_query_stakeholder__resolve_for_group" },
      { action: "api_resolvers_group_drafts_resolve" },
      { action: "api_resolvers_group_billing_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/test/vulns"]}>
        <MockedProvider addTypename={false} mocks={mockedQueries}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "has_squad" }])}
          >
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupContent}
                path={"/orgs/:organizationName/groups/:groupName/vulns"}
              />
            </authzPermissionsContext.Provider>
          </authzGroupContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("link")).toHaveLength(
        numberOfLinksWithPermissions
      );
    });
  });

  it("should prevent access under review", async (): Promise<void> => {
    expect.hasAssertions();

    const orgMock: MockedResponse<IGetOrganizationId> = {
      request: {
        query: GET_ORGANIZATION_ID,
        variables: {
          organizationName: "testorg",
        },
      },
      result: {
        data: {
          organizationId: {
            id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
            name: "testorg",
          },
        },
      },
    };
    const groupMock: MockedResponse<IGroupData> = {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "testgroup",
        },
      },
      result: {
        data: {
          group: {
            businessId: "",
            businessName: "",
            description: "",
            hasForces: true,
            hasMachine: true,
            hasSquad: false,
            language: "",
            managed: "UNDER_REVIEW",
            organization: { name: "" },
            service: "",
            sprintDuration: "",
            sprintStartDate: "",
            subscription: "",
          },
        },
      },
    };

    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/testgroup/vulns"]}>
        <MockedProvider mocks={[orgMock, groupMock]}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "has_squad" }])}
          >
            <authzPermissionsContext.Provider value={new PureAbility([])}>
              <Route
                component={GroupContent}
                path={"/orgs/:organizationName/groups/:groupName/vulns"}
              />
            </authzPermissionsContext.Provider>
          </authzGroupContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await expect(
      screen.findByText("group.accessDenied.title")
    ).resolves.toBeInTheDocument();
    expect(
      screen.queryByText("group.accessDenied.btn")
    ).not.toBeInTheDocument();
  });

  it("should allow dismissing", async (): Promise<void> => {
    expect.hasAssertions();

    const orgMock: MockedResponse<IGetOrganizationId> = {
      request: {
        query: GET_ORGANIZATION_ID,
        variables: {
          organizationName: "testorg",
        },
      },
      result: {
        data: {
          organizationId: {
            id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
            name: "testorg",
          },
        },
      },
    };
    const groupMock: MockedResponse<IGroupData> = {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "testgroup",
        },
      },
      result: {
        data: {
          group: {
            businessId: "",
            businessName: "",
            description: "",
            hasForces: true,
            hasMachine: true,
            hasSquad: false,
            language: "",
            managed: "UNDER_REVIEW",
            organization: { name: "" },
            service: "",
            sprintDuration: "",
            sprintStartDate: "",
            subscription: "",
          },
        },
      },
    };

    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/testgroup/vulns"]}>
        <MockedProvider mocks={[orgMock, groupMock]}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "has_squad" }])}
          >
            <authzPermissionsContext.Provider
              value={
                new PureAbility([
                  { action: "api_mutations_update_group_managed_mutate" },
                ])
              }
            >
              <Route
                component={GroupContent}
                path={"/orgs/:organizationName/groups/:groupName/vulns"}
              />
            </authzPermissionsContext.Provider>
          </authzGroupContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    const continueAccess = await screen.findByText("group.accessDenied.btn");

    expect(continueAccess).toBeInTheDocument();

    await userEvent.click(continueAccess);

    await expect(
      screen.findByText("group.tabs.findings.text")
    ).resolves.toBeInTheDocument();
  });
});
