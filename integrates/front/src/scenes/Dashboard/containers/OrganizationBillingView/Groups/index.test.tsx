import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { OrganizationGroups } from "scenes/Dashboard/containers/OrganizationBillingView/Groups/index";
import { authzPermissionsContext } from "utils/authz/config";

describe("Organization billing groups view", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationGroups).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_subscription_mutate" },
      { action: "api_resolvers_organization_billing_portal_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/okada/billing"]}>
        <MockedProvider addTypename={false} mocks={[]}>
          <Route path={"/orgs/:organizationName/billing"}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <OrganizationGroups
                billingPortal={""}
                groups={[
                  {
                    authors: {
                      currentSpend: 1,
                      total: 1,
                    },
                    forces: "",
                    hasForces: true,
                    hasMachine: true,
                    hasSquad: true,
                    machine: "",
                    managed: true,
                    name: "unittesting",
                    permissions: ["api_mutations_update_subscription_mutate"],
                    service: "WHITE",
                    squad: "true",
                    tier: "SQUAD",
                  },
                ]}
                onUpdate={jest.fn()}
              />
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });

    expect(screen.getAllByRole("row")).toHaveLength(2);
    expect(screen.getAllByRole("button")).toHaveLength(2);

    jest.clearAllMocks();
  });
});
