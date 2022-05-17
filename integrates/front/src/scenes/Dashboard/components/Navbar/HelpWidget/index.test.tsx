import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { HelpModal } from "scenes/Dashboard/components/Navbar/HelpWidget/modal";
import type { IOrganizationGroups } from "scenes/Dashboard/types";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";

describe("HelpModal", (): void => {
  const groups: IOrganizationGroups["groups"] = [
    {
      name: "unittesting",
      permissions: [],
      serviceAttributes: ["has_squad", "is_continuous"],
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof HelpModal).toBe("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
          <authContext.Provider
            value={{
              tours: {
                newGroup: true,
                newRoot: true,
              },
              userEmail: "test@fluidattacks.com",
              userName: "",
            }}
          >
            <Route path={"/orgs/:orgName/groups"}>
              <HelpModal groups={groups} />
            </Route>
          </authContext.Provider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(1);
    });

    userEvent.click(screen.getAllByRole("button")[0]);

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(3);
    });

    userEvent.type(screen.getByText("navbar.help.support"), "{esc}");

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(1);
    });
  });

  it("should render talk expert too", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MemoryRouter
          initialEntries={["/orgs/okada/groups/unittesting/events"]}
        >
          <authContext.Provider
            value={{
              tours: {
                newGroup: true,
                newRoot: true,
              },
              userEmail: "test@fluidattacks.com",
              userName: "",
            }}
          >
            <Route path={"/orgs/:orgName/groups/:groupName/events"}>
              <HelpModal groups={groups} />
            </Route>
          </authContext.Provider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(1);
    });

    userEvent.click(screen.getAllByRole("button")[0]);

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(4);
    });
    userEvent.click(screen.getAllByRole("button")[2]);

    await waitFor((): void => {
      expect(screen.queryByText("upgrade.title")).not.toBeInTheDocument();
    });
  });

  it("should render upgrade modal", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const nonValidGroups: IOrganizationGroups["groups"] = [
      {
        name: "unittesting",
        permissions: [],
        serviceAttributes: [],
      },
    ];
    const { container } = render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <MemoryRouter
          initialEntries={["/orgs/okada/groups/unittesting/events"]}
        >
          <MockedProvider addTypename={true} mocks={[]}>
            <authContext.Provider
              value={{
                tours: {
                  newGroup: true,
                  newRoot: true,
                },
                userEmail: "test@fluidattacks.com",
                userName: "",
              }}
            >
              <Route path={"/orgs/:orgName/groups/:groupName/events"}>
                <HelpModal groups={nonValidGroups} />
              </Route>
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(1);
    });

    userEvent.click(screen.getAllByRole("button")[0]);

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(4);
    });

    userEvent.click(screen.getAllByRole("button")[2]);

    await waitFor((): void => {
      expect(screen.queryByText("upgrade.title")).toBeInTheDocument();
    });

    expect(container.querySelector("#page-region")).not.toBeInTheDocument();
  });
});
