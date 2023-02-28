import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { Navbar } from "scenes/Dashboard/components/Navbar";
import {
  GET_FINDING_TITLE,
  GET_USER_ORGANIZATIONS,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/queries";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";

const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router-dom", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

describe("navbar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Navbar).toBe("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions = new PureAbility<string>([
      { action: "front_can_use_groups_searchbar" },
    ]);
    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_USER_ORGANIZATIONS_GROUPS,
        },
        result: {
          data: {
            me: {
              organizations: {
                groups: [
                  {
                    name: "testgroup",
                    permissions: ["valid_assigned"],
                    serviceAttributes: [],
                  },
                ],
                name: "okada",
              },
            },
          },
        },
      },
      {
        request: {
          query: GET_USER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  groups: [],
                  name: "okada",
                },
                {
                  __typename: "Organization",
                  groups: [],
                  name: "bulat",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    localStorage.setItem("organization", JSON.stringify({ name: "okada" }));

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
          <MockedProvider addTypename={true} mocks={[...mockedQueries]}>
            <authContext.Provider
              value={{
                tours: {
                  newGroup: true,
                  newRiskExposure: true,
                  newRoot: true,
                  welcome: true,
                },
                userEmail: "test@fluidattacks.com",
                userName: "",
              }}
            >
              <Navbar
                allAssigned={0}
                meVulnerabilitiesAssignedIds={undefined}
                undefinedOrEmpty={true}
                userRole={"user"}
              />
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("navbar.searchPlaceholder")
      ).toBeInTheDocument();
    });

    expect(screen.getAllByRole("button")[0].textContent).toBe("Okada\u00a0");
    expect(screen.queryByText("bulat")).not.toBeInTheDocument();

    await userEvent.hover(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(screen.queryByText("Bulat")).toBeInTheDocument();
    });
    await userEvent.unhover(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(screen.queryByText("Bulat")).not.toBeInTheDocument();
    });

    await userEvent.click(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledTimes(0);
    });
    await userEvent.hover(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(screen.queryByText("Bulat")).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText("Bulat"));
    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledTimes(1);
    });

    expect(mockHistoryPush).toHaveBeenCalledWith("/orgs/bulat/groups");

    localStorage.clear();
    jest.clearAllMocks();
  });

  it("should display draft title", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "front_can_use_groups_searchbar" },
    ]);
    const organizationsQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_USER_ORGANIZATIONS,
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            organizations: [
              {
                __typename: "Organization",
                name: "okada",
              },
            ],
            userEmail: "test@fluidattacks.com",
          },
        },
      },
    };
    const findingTitleQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_FINDING_TITLE,
        variables: {
          findingId: "F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF",
        },
      },
      result: {
        data: {
          finding: {
            title: "001. Test draft title",
          },
        },
      },
    };

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter
          initialEntries={[
            "/orgs/okada/groups/unittesting/drafts/F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF/locations",
          ]}
        >
          <MockedProvider
            addTypename={true}
            mocks={[findingTitleQuery, organizationsQuery]}
          >
            <authContext.Provider
              value={{
                tours: {
                  newGroup: true,
                  newRiskExposure: true,
                  newRoot: true,
                  welcome: true,
                },
                userEmail: "test@fluidattacks.com",
                userName: "",
              }}
            >
              <Navbar
                allAssigned={0}
                meVulnerabilitiesAssignedIds={undefined}
                undefinedOrEmpty={true}
                userRole={"user"}
              />
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.getByText("001. Test draft title")).toHaveAttribute(
        "href",
        "/orgs/okada/groups/unittesting/drafts/F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF"
      );
    });
  });

  it("should display finding title", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "front_can_use_groups_searchbar" },
    ]);
    const organizationsQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_USER_ORGANIZATIONS,
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            organizations: [
              {
                __typename: "Organization",
                name: "okada",
              },
            ],
            userEmail: "test@fluidattacks.com",
          },
        },
      },
    };
    const findingTitleQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_FINDING_TITLE,
        variables: {
          findingId: "436992569",
        },
      },
      result: {
        data: {
          finding: {
            title: "001. Test finding title",
          },
        },
      },
    };
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter
          initialEntries={[
            "/orgs/okada/groups/unittesting/vulns/436992569/description",
          ]}
        >
          <MockedProvider
            addTypename={true}
            mocks={[findingTitleQuery, organizationsQuery]}
          >
            <authContext.Provider
              value={{
                tours: {
                  newGroup: true,
                  newRiskExposure: true,
                  newRoot: true,
                  welcome: true,
                },
                userEmail: "test@fluidattacks.com",
                userName: "",
              }}
            >
              <Navbar
                allAssigned={0}
                meVulnerabilitiesAssignedIds={undefined}
                undefinedOrEmpty={true}
                userRole={"user"}
              />
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.getByText("001. Test finding title")).toHaveAttribute(
        "href",
        "/orgs/okada/groups/unittesting/vulns/436992569"
      );
    });
  });
});
