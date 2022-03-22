import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { timeFromNow } from "components/Table/formatters";
import { GroupStakeholdersView } from "scenes/Dashboard/containers/GroupStakeholdersView";
import {
  ADD_STAKEHOLDER_MUTATION,
  GET_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
  UPDATE_GROUP_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/GroupStakeholdersView/queries";
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

describe("Group stakeholders view", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_STAKEHOLDERS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            name: "TEST",
            stakeholders: [
              {
                email: "user@gmail.com",
                firstLogin: "2017-09-05 15:00:00",
                invitationState: "CONFIRMED",
                lastLogin: "2017-10-29 13:40:37",
                responsibility: "Test responsibility",
                role: "user",
              },
            ],
          },
        },
      },
    },
    {
      request: {
        query: GET_STAKEHOLDERS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            name: "TEST",
            stakeholders: [
              {
                email: "user@gmail.com",
                firstLogin: "2017-09-05 15:00:00",
                invitationState: "CONFIRMED",
                lastLogin: "2017-10-29 13:40:37",
                responsibility: "Rest responsibility",
                role: "user",
              },
              {
                email: "unittest@test.com",
                firstLogin: "2017-09-05 15:00:00",
                invitationState: "CONFIRMED",
                lastLogin: "2017-10-29 13:40:37",
                responsibility: "Project Manager",
                role: "hacker",
              },
            ],
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_STAKEHOLDERS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupStakeholdersView).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={GroupStakeholdersView}
            path={"/groups/:groupName/stakeholders"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });

    jest.clearAllMocks();
  });

  it("should display all group stakeholder columns", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={GroupStakeholdersView}
            path={"/groups/:groupName/stakeholders"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.getByText("searchFindings.usersTable.usermail")
    ).toBeInTheDocument();
    expect(
      screen.getByText("searchFindings.usersTable.userRole")
    ).toBeInTheDocument();
    expect(
      screen.getByText("searchFindings.usersTable.userResponsibility")
    ).toBeInTheDocument();
    expect(
      screen.getByText("searchFindings.usersTable.firstlogin")
    ).toBeInTheDocument();
    expect(
      screen.getByText("searchFindings.usersTable.lastlogin")
    ).toBeInTheDocument();
    expect(
      screen.getByText("searchFindings.usersTable.invitation")
    ).toBeInTheDocument();
    expect(screen.getByText("user@gmail.com")).toBeInTheDocument();
    expect(screen.getByText("userModal.roles.user")).toBeInTheDocument();
    expect(screen.getByText("Test responsibility")).toBeInTheDocument();
    expect(screen.getByText("2017-09-05 15:00:00")).toBeInTheDocument();
    expect(
      screen.getByText(timeFromNow("2017-10-29 13:40:37"))
    ).toBeInTheDocument();
    expect(screen.getByText("Confirmed")).toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should render an add stakeholder component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={GroupStakeholdersView}
            path={"/groups/:groupName/stakeholders"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    jest.clearAllMocks();
  });

  it("should render an edit stakeholder component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_grant_stakeholder_access_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.getByText("searchFindings.tabUsers.addButton.text")
    ).toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should open a modal to add stakeholder", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_grant_stakeholder_access_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.title")
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByText("searchFindings.tabUsers.addButton.text"));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.title")
      ).toBeInTheDocument();
    });

    jest.clearAllMocks();
  });

  it("should open a modal to edit stakeholder", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_group_stakeholder_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.editButton.text")
    ).toBeDisabled();

    userEvent.click(screen.getByRole("cell", { name: "user@gmail.com" }));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.editButton.text")
      ).not.toBeDisabled();
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.editStakeholderTitle")
    ).not.toBeInTheDocument();

    userEvent.click(
      screen.getByText("searchFindings.tabUsers.editButton.text")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.editStakeholderTitle")
      ).toBeInTheDocument();
    });

    jest.clearAllMocks();
  });

  it("should add stakeholder to the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_STAKEHOLDER_MUTATION,
          variables: {
            email: "unittest@test.com",
            groupName: "TEST",
            responsibility: "Project Manager",
            role: "HACKER",
          },
        },
        result: {
          data: {
            grantStakeholderAccess: {
              grantedStakeholder: {
                email: "unittest@test.com",
                firstLogin: "",
                lastLogin: "",
                responsibility: "Project Manager",
                role: "HACKER",
              },
              success: true,
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_grant_stakeholder_access_mutate" },
      { action: "grant_group_level_role:hacker" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks.concat(mocksMutation)}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.title")
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByText("searchFindings.tabUsers.addButton.text"));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.title")
      ).toBeInTheDocument();
    });

    userEvent.type(
      screen.getByRole("textbox", { name: "email" }),
      "unittest@test.com"
    );
    userEvent.type(
      screen.getByRole("textbox", { name: "responsibility" }),
      "Project Manager"
    );
    userEvent.selectOptions(screen.getByRole("combobox", { name: "role" }), [
      "HACKER",
    ]);
    await waitFor((): void => {
      expect(screen.queryByText("Proceed")).not.toBeDisabled();
    });
    userEvent.click(screen.getByText("Proceed"));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.title")
    ).not.toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should remove stakeholder from the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_STAKEHOLDER_MUTATION,
          variables: {
            groupName: "TEST",
            userEmail: "user@gmail.com",
          },
        },
        result: {
          data: {
            removeStakeholderAccess: {
              removedEmail: "user@gmail.com",
              success: true,
            },
          },
        },
      },
    ];
    const mockResult: readonly MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDERS,
          variables: {
            groupName: "TEST",
          },
        },
        result: {
          data: {
            group: {
              name: "TEST",
              stakeholders: [
                {
                  email: "unittest@test.com",
                  firstLogin: "2017-09-05 15:00:00",
                  invitationState: "CONFIRMED",
                  lastLogin: "2017-10-29 13:40:37",
                  responsibility: "Project Manager",
                  role: "hacker",
                },
              ],
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_stakeholder_access_mutate" },
      { action: "api_mutations_update_group_stakeholder_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider
          addTypename={false}
          mocks={[...[mocks[1]], ...mocksMutation, ...mockResult]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getAllByRole("radio", { checked: false })).toHaveLength(2);
    expect(
      screen.queryByText("searchFindings.tabUsers.removeUserButton.text")
    ).toBeDisabled();

    userEvent.click(screen.getByRole("cell", { name: "user@gmail.com" }));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.removeUserButton.text")
      ).not.toBeDisabled();
    });

    expect(screen.getAllByRole("radio", { checked: false })).toHaveLength(1);
    expect(screen.getAllByRole("radio", { checked: true })).toHaveLength(1);

    userEvent.click(
      screen.getByText("searchFindings.tabUsers.removeUserButton.text")
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });

    expect(screen.getAllByRole("radio", { checked: false })).toHaveLength(1);
    expect(screen.queryAllByRole("radio", { checked: true })).toHaveLength(0);

    jest.clearAllMocks();
  });

  it("should edit stakeholder from the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: UPDATE_GROUP_STAKEHOLDER_MUTATION,
          variables: {
            email: "user@gmail.com",
            groupName: "TEST",
            responsibility: "Project Manager",
            role: "HACKER",
          },
        },
        result: {
          data: {
            updateGroupStakeholder: {
              success: true,
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_group_stakeholder_mutate" },
      { action: "grant_group_level_role:hacker" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks.concat(mocksMutation)}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.editButton.text")
    ).toBeDisabled();

    userEvent.click(screen.getByRole("cell", { name: "user@gmail.com" }));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.editButton.text")
      ).not.toBeDisabled();
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.editStakeholderTitle")
    ).not.toBeInTheDocument();

    userEvent.click(
      screen.getByText("searchFindings.tabUsers.editButton.text")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.editStakeholderTitle")
      ).toBeInTheDocument();
    });
    userEvent.clear(screen.getByRole("textbox", { name: "responsibility" }));
    userEvent.type(
      screen.getByRole("textbox", { name: "responsibility" }),
      "Project Manager"
    );
    userEvent.selectOptions(screen.getByRole("combobox", { name: "role" }), [
      "HACKER",
    ]);
    await waitFor((): void => {
      expect(screen.queryByText("Proceed")).not.toBeDisabled();
    });
    userEvent.click(screen.getByText("Proceed"));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.title")
    ).not.toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should handle errors when adding a stakeholder to the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_STAKEHOLDER_MUTATION,
          variables: {
            email: "unittest@test.com",
            groupName: "TEST",
            responsibility: "Project Manager",
            role: "HACKER",
          },
        },
        result: {
          errors: [
            new GraphQLError("Access denied"),
            new GraphQLError("Exception - Email is not valid"),
            new GraphQLError("Exception - Invalid field in form"),
            new GraphQLError("Exception - Invalid characters"),
            new GraphQLError("Exception - Invalid email address in form"),
            new GraphQLError(
              "Exception - Groups without an active Fluid Attacks service " +
                "can not have Fluid Attacks staff"
            ),
            new GraphQLError(
              "Exception - Groups with any active Fluid Attacks service " +
                "can only have Hackers provided by Fluid Attacks"
            ),
          ],
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_grant_stakeholder_access_mutate" },
      { action: "grant_group_level_role:hacker" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks.concat(mocksMutation)}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.title")
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByText("searchFindings.tabUsers.addButton.text"));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.title")
      ).toBeInTheDocument();
    });

    userEvent.type(
      screen.getByRole("textbox", { name: "email" }),
      "unittest@test.com"
    );
    userEvent.type(
      screen.getByRole("textbox", { name: "responsibility" }),
      "Project Manager"
    );
    userEvent.selectOptions(screen.getByRole("combobox", { name: "role" }), [
      "HACKER",
    ]);
    await waitFor((): void => {
      expect(screen.queryByText("Proceed")).not.toBeDisabled();
    });
    userEvent.click(screen.getByText("Proceed"));

    const TEST_TIMES_CALLED = 7;
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(TEST_TIMES_CALLED);
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.title")
    ).not.toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should handle error when removing a stakeholder from the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_STAKEHOLDER_MUTATION,
          variables: {
            groupName: "TEST",
            userEmail: "user@gmail.com",
          },
        },
        result: { errors: [new GraphQLError("Access denied")] },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_stakeholder_access_mutate" },
      { action: "api_mutations_update_group_stakeholder_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks.concat(mocksMutation)}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getAllByRole("radio", { checked: false })).toHaveLength(1);
    expect(
      screen.queryByText("searchFindings.tabUsers.removeUserButton.text")
    ).toBeDisabled();

    userEvent.click(screen.getByRole("cell", { name: "user@gmail.com" }));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.removeUserButton.text")
      ).not.toBeDisabled();
    });

    expect(screen.queryAllByRole("radio", { checked: false })).toHaveLength(0);
    expect(screen.getAllByRole("radio", { checked: true })).toHaveLength(1);

    userEvent.click(
      screen.getByText("searchFindings.tabUsers.removeUserButton.text")
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.title")
    ).not.toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should handle error when editing a stakeholder from the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: UPDATE_GROUP_STAKEHOLDER_MUTATION,
          variables: {
            email: "user@gmail.com",
            groupName: "TEST",
            responsibility: "Project Manager",
            role: "HACKER",
          },
        },
        result: {
          errors: [
            new GraphQLError("Access denied"),
            new GraphQLError("Exception - Invalid field in form"),
            new GraphQLError("Exception - Invalid characters"),
            new GraphQLError(
              "Exception - Groups without an active Fluid Attacks service " +
                "can not have Fluid Attacks staff"
            ),
            new GraphQLError(
              "Exception - Groups with any active Fluid Attacks service " +
                "can only have Hackers provided by Fluid Attacks"
            ),
          ],
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_group_stakeholder_mutate" },
      { action: "grant_group_level_role:hacker" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <MockedProvider addTypename={false} mocks={mocks.concat(mocksMutation)}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.editButton.text")
    ).toBeDisabled();

    userEvent.click(screen.getByRole("cell", { name: "user@gmail.com" }));
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.editButton.text")
      ).not.toBeDisabled();
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.editStakeholderTitle")
    ).not.toBeInTheDocument();

    userEvent.click(
      screen.getByText("searchFindings.tabUsers.editButton.text")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabUsers.editStakeholderTitle")
      ).toBeInTheDocument();
    });
    userEvent.clear(screen.getByRole("textbox", { name: "responsibility" }));
    userEvent.type(
      screen.getByRole("textbox", { name: "responsibility" }),
      "Project Manager"
    );
    userEvent.selectOptions(screen.getByRole("combobox", { name: "role" }), [
      "HACKER",
    ]);
    await waitFor((): void => {
      expect(screen.queryByText("Proceed")).not.toBeDisabled();
    });
    userEvent.click(screen.getByText("Proceed"));
    const TEST_TIMES_CALLED = 5;

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(TEST_TIMES_CALLED);
    });

    expect(
      screen.queryByText("searchFindings.tabUsers.title")
    ).not.toBeInTheDocument();

    jest.clearAllMocks();
  });
});
