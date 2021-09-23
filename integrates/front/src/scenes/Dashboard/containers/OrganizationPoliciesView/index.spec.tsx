import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { OrganizationPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView";
import {
  GET_ORGANIZATION_POLICIES,
  UPDATE_ORGANIZATION_POLICIES,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import type { IOrganizationPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Organization policies view", (): void => {
  const mockProps: IOrganizationPolicies = {
    organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
  };

  it("should return a  function", (): void => {
    expect.hasAssertions();

    expect(typeof OrganizationPolicies).toStrictEqual("function");
  });

  it("should render component with default values", async (): Promise<void> => {
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
              maxAcceptanceDays: null,
              maxAcceptanceSeverity: 10,
              maxNumberAcceptations: null,
              minAcceptanceSeverity: 0,
              name: "okada",
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/policies"}>
            <OrganizationPolicies organizationId={mockProps.organizationId} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("tr")).toHaveLength(4);
      });
    });

    expect(
      wrapper.find({ name: "maxAcceptanceDays" }).find("input").prop("value")
    ).toBe("");

    expect(
      wrapper
        .find({ name: "maxAcceptanceSeverity" })
        .find("input")
        .prop("value")
    ).toBe("10.0");

    expect(
      wrapper
        .find({ name: "maxNumberAcceptations" })
        .find("input")
        .prop("value")
    ).toBe("");

    expect(
      wrapper
        .find({ name: "minAcceptanceSeverity" })
        .find("input")
        .prop("value")
    ).toBe("0.0");
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
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/policies"}>
            <OrganizationPolicies organizationId={mockProps.organizationId} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledTimes(1);
        expect(wrapper.find("table")).toHaveLength(0);
      });
    });
  });

  it("should update the policies", async (): Promise<void> => {
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
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptations: 5,
              minAcceptanceSeverity: 3,
              name: "okada",
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            maxAcceptanceDays: 2,
            maxAcceptanceSeverity: 8.9,
            maxNumberAcceptations: 1,
            minAcceptanceSeverity: 0,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
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
              maxAcceptanceDays: 2,
              maxAcceptanceSeverity: 8.9,
              maxNumberAcceptations: 1,
              minAcceptanceSeverity: 0,
              name: "okada",
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_organization_policies_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
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

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("tr")).toHaveLength(4);
      });
    });

    const maxAcceptanceDays: ReactWrapper = wrapper
      .find({ name: "maxAcceptanceDays" })
      .find("input");
    const maxAcceptanceSeverity: ReactWrapper = wrapper
      .find({ name: "maxAcceptanceSeverity" })
      .find("input");
    const maxNumberAcceptations: ReactWrapper = wrapper
      .find({ name: "maxNumberAcceptations" })
      .find("input");
    const minAcceptanceSeverity: ReactWrapper = wrapper
      .find({ name: "minAcceptanceSeverity" })
      .find("input");
    const saveButton1: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean => element.contains("Save"))
      .first();

    expect(saveButton1).toHaveLength(0);

    maxAcceptanceDays.simulate("change", {
      target: { name: "maxAcceptanceDays", value: "2" },
    });
    maxAcceptanceSeverity.simulate("change", {
      target: { name: "maxAcceptanceSeverity", value: "8.9" },
    });
    maxNumberAcceptations.simulate("change", {
      target: { name: "maxNumberAcceptations", value: "1" },
    });
    minAcceptanceSeverity.simulate("change", {
      target: { name: "minAcceptanceSeverity", value: "0" },
    });

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        const saveButton2: ReactWrapper = wrapper
          .find("button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.contains("Save")
          )
          .first();

        expect(saveButton2).toHaveLength(1);
      });
    });

    const form: ReactWrapper = wrapper.find({ name: "orgPolicies" });

    form.simulate("submit");

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(msgSuccess).toHaveBeenCalledTimes(1);
        expect(
          wrapper
            .find({ name: "maxAcceptanceDays" })
            .find("input")
            .prop("value")
        ).toBe("2");
      });
    });
  });

  it("should not show save button", async (): Promise<void> => {
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
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptations: 2,
              minAcceptanceSeverity: 3,
              name: "okada",
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/policies"}>
            <OrganizationPolicies organizationId={mockProps.organizationId} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("tr")).toHaveLength(4);
      });
    });

    const maxAcceptanceDays: ReactWrapper = wrapper
      .find({ name: "maxAcceptanceDays" })
      .find("input");
    const saveButton1: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper): boolean => element.contains("Save"))
      .first();

    expect(saveButton1).toHaveLength(0);

    maxAcceptanceDays.simulate("change", { target: { value: "2" } });

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        const saveButton2: ReactWrapper = wrapper
          .find("button")
          .filterWhere((element: ReactWrapper): boolean =>
            element.contains("Save")
          )
          .first();

        expect(saveButton2).toHaveLength(0);
      });
    });
  });

  it("should handle errors", async (): Promise<void> => {
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
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptations: 2,
              minAcceptanceSeverity: 3,
              name: "okada",
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptations: 2,
            minAcceptanceSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
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
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptations: 2,
            minAcceptanceSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Severity value should be a positive floating number between 0.0 a 10.0"
            ),
          ],
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptations: 2,
            minAcceptanceSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
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
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptations: 2,
            minAcceptanceSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Number of acceptations should be zero or positive"
            ),
          ],
        },
      },
      {
        request: {
          query: UPDATE_ORGANIZATION_POLICIES,
          variables: {
            maxAcceptanceDays: 1,
            maxAcceptanceSeverity: 7.5,
            maxNumberAcceptations: 2,
            minAcceptanceSeverity: 3,
            organizationId: mockProps.organizationId,
            organizationName: "okada",
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_organization_policies_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
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

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("tr")).toHaveLength(4);
      });
    });

    const form: ReactWrapper = wrapper.find({ name: "orgPolicies" });
    const maxAcceptanceDays: ReactWrapper = wrapper
      .find({ name: "maxAcceptanceDays" })
      .find("input");

    maxAcceptanceDays.simulate("change", {
      target: { name: "maxAcceptanceDays", value: "1" },
    });
    form.simulate("submit");

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t("organization.tabs.policies.errors.maxAcceptanceDays")
        );
      });
    });

    form.simulate("submit");

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t("organization.tabs.policies.errors.acceptanceSeverity")
        );
      });
    });

    form.simulate("submit");

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t(
            "organization.tabs.policies.errors.acceptanceSeverityRange"
          )
        );
      });
    });

    form.simulate("submit");

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t("organization.tabs.policies.errors.maxNumberAcceptations")
        );
      });
    });

    form.simulate("submit");

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(msgError).toHaveBeenCalledWith(
          translate.t("groupAlerts.errorTextsad")
        );
      });
    });
  });
});
