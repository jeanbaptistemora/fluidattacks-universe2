import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_GROUP_SERVICES } from "./queries";

import { HelpModal } from ".";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";

describe("helpModal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof HelpModal).toBe("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const mockedQueries: MockedResponse[] = [
      {
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
                      name: "unittesting",
                      permissions: [],
                      serviceAttributes: ["has_squad", "is_continuous"],
                    },
                  ],
                  name: "okada",
                },
              ],
              userEmail: "",
            },
          },
        },
      },
    ];

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
          <MockedProvider addTypename={true} mocks={[...mockedQueries]}>
            <authContext.Provider
              value={{
                tours: {
                  newGroup: true,
                  newRiskExposure: true,
                  newRoot: true,
                },
                userEmail: "test@fluidattacks.com",
                userName: "",
              }}
            >
              <Route path={"/orgs/:orgName/groups"}>
                <HelpModal open={true} />
              </Route>
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(4);
    });
  });

  it("should render talk expert too", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_GROUP_SERVICES,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              name: "unittesting",
              serviceAttributes: [],
            },
          },
        },
      },
      {
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
                      name: "unittesting",
                      permissions: [],
                      serviceAttributes: ["has_squad", "is_continuous"],
                    },
                  ],
                  name: "okada",
                },
              ],
              userEmail: "",
            },
          },
        },
      },
    ];

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MemoryRouter
          initialEntries={["/orgs/okada/groups/unittesting/events"]}
        >
          <MockedProvider addTypename={true} mocks={[...mockedQueries]}>
            <authContext.Provider
              value={{
                tours: {
                  newGroup: true,
                  newRiskExposure: true,
                  newRoot: true,
                },
                userEmail: "test@fluidattacks.com",
                userName: "",
              }}
            >
              <Route path={"/orgs/:orgName/groups/:groupName/events"}>
                <HelpModal open={true} />
              </Route>
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(6);
    });
    await userEvent.click(screen.getAllByRole("button")[3]);

    await waitFor((): void => {
      expect(screen.queryByText("upgrade.title")).not.toBeInTheDocument();
    });
  });

  it("should render upgrade modal", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_GROUP_SERVICES,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              name: "unittesting",
              serviceAttributes: [],
            },
          },
        },
      },
      {
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
                      name: "unittesting",
                      permissions: [],
                      serviceAttributes: [],
                    },
                  ],
                  name: "okada",
                },
              ],
              userEmail: "",
            },
          },
        },
      },
    ];
    const { container } = render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MemoryRouter
          initialEntries={["/orgs/okada/groups/unittesting/events"]}
        >
          <MockedProvider addTypename={true} mocks={[...mockedQueries]}>
            <authContext.Provider
              value={{
                tours: {
                  newGroup: true,
                  newRiskExposure: true,
                  newRoot: true,
                },
                userEmail: "test@fluidattacks.com",
                userName: "",
              }}
            >
              <Route path={"/orgs/:orgName/groups/:groupName/events"}>
                <HelpModal open={true} />
              </Route>
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(6);
    });

    await userEvent.click(screen.getAllByRole("button")[2]);

    await waitFor((): void => {
      expect(screen.queryByText("upgrade.title")).toBeInTheDocument();
    });

    expect(container.querySelector("#page-region")).not.toBeInTheDocument();
  });
});
