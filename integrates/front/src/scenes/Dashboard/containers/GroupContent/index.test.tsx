import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupContent } from "scenes/Dashboard/containers/GroupContent";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

describe("GroupContent", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupContent).toBe("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const numberOfLinks: number = 5;
    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/test/vulns"]}>
        <MockedProvider addTypename={false} mocks={[]}>
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

    const numberOfLinksWithPermissions: number = 8;
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_group_consulting_resolve" },
      { action: "api_resolvers_query_stakeholder__resolve_for_group" },
      { action: "api_resolvers_group_drafts_resolve" },
      { action: "api_resolvers_group_authors_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/test/vulns"]}>
        <MockedProvider addTypename={false} mocks={[]}>
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
});
