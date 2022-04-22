import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import { GraphQLError } from "graphql";
import { set } from "mockdate";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupAuthorsView } from "scenes/Dashboard/containers/GroupAuthorsView";
import { GET_BILLING } from "scenes/Dashboard/containers/GroupAuthorsView/queries";
import { GET_STAKEHOLDERS } from "scenes/Dashboard/containers/GroupStakeholdersView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

describe("AuthorsView", (): void => {
  const TEST_DATE = 2020;
  const date: Date = new Date(TEST_DATE, 0);
  set(date);
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_BILLING,
        variables: {
          date: date.toISOString(),
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            authors: {
              data: [
                {
                  actor: "test",
                  commit: "123",
                  groups: "test, test2",
                  organization: "testorg",
                  repository: "test_repository",
                },
              ],
            },
            name: "unittesting",
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_BILLING,
        variables: {
          date: date.toISOString(),
          groupName: "unittesting",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupAuthorsView).toBe("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MemoryRouter
          initialEntries={["/orgs/okada/groups/unittesting/authors"]}
        >
          <MockedProvider addTypename={false} mocks={mockError}>
            <Route
              component={GroupAuthorsView}
              path={"/orgs/:organizationName/groups/:groupName/authors"}
            />
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    jest.clearAllMocks();
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MemoryRouter
          initialEntries={["/orgs/okada/groups/unittesting/authors"]}
        >
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route
              component={GroupAuthorsView}
              path={"/orgs/:organizationName/groups/:groupName/authors"}
            />
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getAllByRole("columnheader")).toHaveLength(4);
    expect(screen.getAllByRole("row")[0].textContent).toStrictEqual(
      [
        "group.authors.actor",
        "group.authors.groupsContributed",
        "group.authors.commit",
        "group.authors.repository",
      ].join("")
    );

    jest.clearAllMocks();
  });

  it("should render table", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_grant_stakeholder_access_mutate" },
      { action: "api_resolvers_query_stakeholder__resolve_for_group" },
    ]);
    const mocksStakeholder: MockedResponse = {
      request: {
        query: GET_STAKEHOLDERS,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            name: "unittesting",
            stakeholders: [
              {
                email: "user@gmail.com",
                firstLogin: "2017-09-05 15:00:00",
                invitationState: "CONFIRMED",
                lastLogin: "2017-10-29 13:40:37",
                responsibility: "Rest responsibility",
                role: "user",
              },
            ],
          },
        },
      },
    };

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter
          initialEntries={["/orgs/okada/groups/unittesting/authors"]}
        >
          <MockedProvider
            addTypename={false}
            mocks={[...mocks, mocksStakeholder]}
          >
            <Route
              component={GroupAuthorsView}
              path={"/orgs/:organizationName/groups/:groupName/authors"}
            />
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    const TEST_COLUMN_LENGTH = 5;
    await waitFor((): void => {
      expect(screen.queryAllByRole("columnheader")).toHaveLength(
        TEST_COLUMN_LENGTH
      );
    });

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getAllByRole("row")[0].textContent).toStrictEqual(
      [
        "group.authors.actor",
        "group.authors.groupsContributed",
        "group.authors.commit",
        "group.authors.repository",
        "group.authors.invitationState.confirmed",
      ].join("")
    );
    expect(screen.getAllByRole("cell")[0].textContent).toBe("test");
    expect(screen.getAllByRole("cell")[1].textContent).toStrictEqual(
      "test, test2"
    );
    expect(screen.getAllByRole("cell")[2].textContent).toBe("123");
    expect(
      screen.getAllByRole("cell")[TEST_COLUMN_LENGTH - 2].textContent
    ).toBe("test_repository");
    expect(
      within(screen.getAllByRole("cell")[TEST_COLUMN_LENGTH - 2]).queryByText(
        "group.authors.sendInvitation"
      )
    ).not.toBeInTheDocument();
    expect(
      within(screen.getAllByRole("cell")[TEST_COLUMN_LENGTH - 1]).getByText(
        "group.authors.sendInvitation"
      )
    ).toBeInTheDocument();
  });

  jest.clearAllMocks();
});
