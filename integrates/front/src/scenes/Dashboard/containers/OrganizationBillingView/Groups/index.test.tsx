import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { UPDATE_GROUP_MUTATION } from "../queries";
import { OrganizationGroups } from "scenes/Dashboard/containers/OrganizationBillingView/Groups/index";
import { authzPermissionsContext } from "utils/authz/config";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Organization billing groups view", (): void => {
  const btnConfirm = "components.modal.confirm";

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationGroups).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockMutation: MockedResponse = {
      request: {
        query: UPDATE_GROUP_MUTATION,
        variables: {
          comments: "",
          groupName: "unittesting",
          isManagedChanged: true,
          isPaymentIdChanged: false,
          isSubscriptionChanged: false,
          managed: "NOT_MANUALLY",
          paymentId: "280fe281-e190-45af-b733-a24889b96fd1",
          subscription: "SQUAD",
        },
      },
      result: {
        data: {
          updateGroupManaged: {
            success: true,
          },
        },
      },
    };

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_subscription_mutate" },
      { action: "api_mutations_update_group_managed_mutate" },
      { action: "api_resolvers_organization_billing_portal_resolve" },
      { action: "see_billing_subscription_type" },
      { action: "see_billing_service_type" },
    ]);
    const onUpdate: jest.Mock = jest.fn();
    render(
      <MemoryRouter initialEntries={["/orgs/okada/billing"]}>
        <MockedProvider addTypename={false} mocks={[mockMutation]}>
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
                    managed: "MANUALLY",
                    name: "unittesting",
                    paymentId: "280fe281-e190-45af-b733-a24889b96fd1",
                    permissions: [
                      "api_mutations_update_subscription_mutate",
                      "api_mutations_update_group_managed_mutate",
                    ],
                    service: "WHITE",
                    squad: "true",
                    tier: "SQUAD",
                  },
                ]}
                onUpdate={onUpdate}
                paymentMethods={[]}
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
    expect(screen.queryByText("Manually")).toBeInTheDocument();
    expect(
      screen.queryByText(
        "organization.tabs.billing.groups.updateSubscription.title"
      )
    ).not.toBeInTheDocument();
    expect(screen.queryByText("Tier")).toBeInTheDocument();
    expect(screen.queryByText("Service")).toBeInTheDocument();

    userEvent.click(screen.getByText("Manually"));

    await waitFor((): void => {
      expect(
        screen.queryByText(
          "organization.tabs.billing.groups.updateSubscription.title"
        )
      ).toBeInTheDocument();
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    jest.clearAllMocks();
  });
});
