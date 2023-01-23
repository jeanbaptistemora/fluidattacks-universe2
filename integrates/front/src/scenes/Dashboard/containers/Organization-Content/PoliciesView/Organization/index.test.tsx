/* eslint-disable jest/no-disabled-tests */
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { OrganizationPolicies } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Organization";
import {
  GET_ORGANIZATION_POLICIES,
  UPDATE_ORGANIZATION_POLICIES,
} from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Organization/queries";
import type { IOrganizationPolicies } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Organization/types";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("Organization policies view", (): void => {
  const mockProps: IOrganizationPolicies = {
    organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
  };

  const orgPolicyFields: number = 8;

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof OrganizationPolicies).toBe("function");
  });

  it.skip("should render with default values", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              findingPolicies: [],
              inactivityPeriod: 90,
              maxAcceptanceDays: null,
              maxAcceptanceSeverity: 10,
              maxNumberAcceptances: null,
              minAcceptanceSeverity: 0,
              minBreakingSeverity: 0,
              name: "okada",
              vulnerabilityGracePeriod: 1,
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/policies"}>
            <OrganizationPolicies organizationId={mockProps.organizationId} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getAllByRole("textbox")).toHaveLength(orgPolicyFields);
    });

    expect(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" })
    ).toHaveValue("");
    expect(
      screen.getByRole("textbox", { name: "maxAcceptanceSeverity" })
    ).toHaveValue("10.0");
    expect(
      screen.getByRole("textbox", { name: "maxNumberAcceptances" })
    ).toHaveValue("");
    expect(
      screen.getByRole("textbox", { name: "minAcceptanceSeverity" })
    ).toHaveValue("0.0");
    expect(
      screen.getByRole("textbox", { name: "minBreakingSeverity" })
    ).toHaveValue("0.0");
    expect(
      screen.getByRole("textbox", { name: "vulnerabilityGracePeriod" })
    ).toHaveValue("1");
    expect(
      screen.getByRole("textbox", { name: "inactivityPeriod" })
    ).toHaveValue("90");
  });

  it("should render an error message", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          errors: [new GraphQLError("An error occurred")],
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/policies"}>
            <OrganizationPolicies organizationId={mockProps.organizationId} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });

    expect(screen.queryAllByRole("table")).toHaveLength(0);
  });

  it.skip("should update the policies", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              findingPolicies: [],
              inactivityPolicies: 90,
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptances: 5,
              minAcceptanceSeverity: 3,
              minBreakingSeverity: 1,
              name: "okada",
              vulnerabilityGracePeriod: 1,
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            inactivityPeriod: 180,
            maxAcceptanceDays: 2,
            maxAcceptanceSeverity: 8.9,
            maxNumberAcceptances: 1,
            minAcceptanceSeverity: 0,
            minBreakingSeverity: 4,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
            vulnerabilityGracePeriod: 2,
          },
        },
        result: {
          data: {
            updateOrganizationPolicies: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              findingPolicies: [],
              inactivityPeriod: 180,
              maxAcceptanceDays: 2,
              maxAcceptanceSeverity: 8.9,
              maxNumberAcceptances: 1,
              minAcceptanceSeverity: 0,
              minBreakingSeverity: 4,
              name: "okada",
              vulnerabilityGracePeriod: 2,
            },
          },
        },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_organization_policies_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/policies"}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <OrganizationPolicies organizationId={mockProps.organizationId} />
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getAllByRole("textbox")).toHaveLength(orgPolicyFields);
    });

    expect(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" })
    ).toHaveValue("5");
    expect(
      screen.queryByText("organization.tabs.policies.save")
    ).not.toBeInTheDocument();

    await Promise.all(screen.getAllByRole("textbox").map(userEvent.clear));
    await userEvent.type(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" }),
      "2"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "maxAcceptanceSeverity" }),
      "8.9"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "maxNumberAcceptances" }),
      "1"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "minAcceptanceSeverity" }),
      "0"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "minBreakingSeverity" }),
      "4"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "vulnerabilityGracePeriod" }),
      "2"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "inactivityPeriod" }),
      "180"
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("organization.tabs.policies.save")
      ).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText("organization.tabs.policies.save"));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });

    expect(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" })
    ).toHaveValue("2");
    expect(
      screen.getByRole("textbox", { name: "inactivityPeriod" })
    ).toHaveValue("180");
  });

  it.skip("should not show save button", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              findingPolicies: [],
              inactivityPeriod: 90,
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptances: 2,
              minAcceptanceSeverity: 3,
              minBreakingSeverity: 3,
              name: "okada",
              vulnerabilityGracePeriod: 1,
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/policies"}>
            <OrganizationPolicies organizationId={mockProps.organizationId} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getAllByRole("textbox")).toHaveLength(orgPolicyFields);
    });

    expect(
      screen.queryByText("organization.tabs.policies.save")
    ).not.toBeInTheDocument();

    await userEvent.clear(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" }),
      "2"
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("organization.tabs.policies.save")
      ).not.toBeInTheDocument();
    });
  });

  it.skip("should handle errors", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              findingPolicies: [],
              inactivityPeriod: 90,
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptances: 2,
              minAcceptanceSeverity: 3,
              minBreakingSeverity: 3,
              name: "okada",
              vulnerabilityGracePeriod: 1,
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            inactivityPeriod: 180,
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptances: 2,
            minAcceptanceSeverity: 3,
            minBreakingSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
            vulnerabilityGracePeriod: 1,
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Acceptance days should be a positive integer"
            ),
          ],
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            inactivityPeriod: 180,
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptances: 2,
            minAcceptanceSeverity: 3,
            minBreakingSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
            vulnerabilityGracePeriod: 1,
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Severity value must be a positive floating number between 0.0 and 10.0"
            ),
          ],
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            inactivityPeriod: 180,
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptances: 2,
            minAcceptanceSeverity: 3,
            minBreakingSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
            vulnerabilityGracePeriod: 1,
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Min acceptance severity value should not be higher than the max value"
            ),
          ],
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            inactivityPeriod: 90,
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptances: 2,
            minAcceptanceSeverity: 3,
            minBreakingSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
            vulnerabilityGracePeriod: 1,
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Number of acceptances should be zero or positive"
            ),
          ],
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            inactivityPeriod: 90,
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptances: 2,
            minAcceptanceSeverity: 3,
            minBreakingSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
            vulnerabilityGracePeriod: 1,
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Severity value must be between 0.0 and 10.0"
            ),
          ],
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            inactivityPeriod: 90,
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptances: 2,
            minAcceptanceSeverity: 3,
            minBreakingSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
            vulnerabilityGracePeriod: 1,
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Vulnerability grace period value should be a positive integer"
            ),
          ],
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            inactivityPeriod: 20,
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptances: 2,
            minAcceptanceSeverity: 3,
            minBreakingSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
            vulnerabilityGracePeriod: 1,
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Inactivity period should be greater than the provided value"
            ),
          ],
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            inactivityPeriod: 90,
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptances: 2,
            minAcceptanceSeverity: 3,
            minBreakingSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
            vulnerabilityGracePeriod: 1,
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_organization_policies_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/policies"}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <OrganizationPolicies organizationId={mockProps.organizationId} />
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getAllByRole("textbox")).toHaveLength(orgPolicyFields);
    });

    await userEvent.clear(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" }),
      "1"
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("organization.tabs.policies.save")
      ).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText("organization.tabs.policies.save"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "organization.tabs.policies.errors.maxAcceptanceDays"
      );
    });

    await userEvent.click(screen.getByText("organization.tabs.policies.save"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "organization.tabs.policies.errors.acceptanceSeverity"
      );
    });

    await userEvent.click(screen.getByText("organization.tabs.policies.save"));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "organization.tabs.policies.errors.acceptanceSeverityRange"
      );
    });

    await userEvent.click(screen.getByText("organization.tabs.policies.save"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "organization.tabs.policies.errors.maxNumberAcceptances"
      );
    });

    await userEvent.click(screen.getByText("organization.tabs.policies.save"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "organization.tabs.policies.errors.invalidBreakableSeverity"
      );
    });

    await userEvent.click(screen.getByText("organization.tabs.policies.save"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "organization.tabs.policies.errors.inactivityPeriod"
      );
    });

    await userEvent.click(screen.getByText("organization.tabs.policies.save"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
  });
});
