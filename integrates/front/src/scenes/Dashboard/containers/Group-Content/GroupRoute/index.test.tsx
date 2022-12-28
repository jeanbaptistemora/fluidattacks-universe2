import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_ORGANIZATION_ID } from "../../Organization-Content/OrganizationNav/queries";
import { GroupRoute } from "scenes/Dashboard/containers/Group-Content/GroupRoute";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/Group-Content/GroupRoute/queries";
import { GET_GROUP_LEVEL_PERMISSIONS } from "scenes/Dashboard/queries";
import { msgError } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

describe("groupRoute", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupRoute).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_GROUP_DATA,
          variables: {
            groupName: "test",
          },
        },
        result: {
          data: {
            group: {
              name: "test",
              organization: "okada",
              serviceAttributes: ["has_asm"],
              userDeletion: "",
            },
          },
        },
      },
      {
        request: {
          query: GET_GROUP_LEVEL_PERMISSIONS,
          variables: {
            identifier: "test",
          },
        },
        result: {
          data: {
            group: {
              name: "test",
              permissions: [],
              userRole: "user",
            },
          },
        },
      },
      {
        request: {
          query: GET_ORGANIZATION_ID,
          variables: {
            organizationName: "okada",
          },
        },
        result: {
          data: {
            organizationId: {
              id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
              name: "okada",
            },
          },
        },
      },
    ];

    const setUserRoleCallback: jest.Mock = jest.fn();
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/test"]}>
        <MockedProvider addTypename={false} mocks={mockedQueries}>
          <Route path={"/orgs/:organizationName/groups/:groupName"}>
            <GroupRoute setUserRole={setUserRoleCallback} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(setUserRoleCallback).toHaveBeenCalledWith("user");
    });
    const numberOfTabs: number = 5;

    await expect(screen.findAllByRole("listitem")).resolves.toHaveLength(
      numberOfTabs
    );

    jest.clearAllMocks();
  });

  it("should render error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockError: MockedResponse[] = [
      {
        request: {
          query: GET_GROUP_DATA,
          variables: {
            groupName: "test",
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    const setUserRoleCallback: jest.Mock = jest.fn();
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/test"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route path={"/orgs/:organizationName/groups/:groupName"}>
            <GroupRoute setUserRole={setUserRoleCallback} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    jest.clearAllMocks();
  });
});
