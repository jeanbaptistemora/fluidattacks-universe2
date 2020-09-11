import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import waitForExpect from "wait-for-expect";

import { OrganizationPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView";
import {
  GET_ORGANIZATION_POLICIES,
  UPDATE_ORGANIZATION_POLICIES,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import { IOrganizationPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView/types";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});

describe("Organization policies view", () => {
  const mockProps: IOrganizationPolicies = { organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3" };

  it("should return a  function", () => {
    expect(typeof OrganizationPolicies)
      .toEqual("function");
  });

  it("should render component with default values", async (): Promise<void> => {
    const mocks: ReadonlyArray<MockedResponse> = [
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
              // tslint:disable: no-null-keyword
              maxAcceptanceDays: null,
              maxAcceptanceSeverity: 10,
              maxNumberAcceptations: null,
              minAcceptanceSeverity: 0,
              // tslint:enable: no-null-keyword
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura/policies"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route path="/orgs/:organizationName/policies">
              <OrganizationPolicies {...mockProps} />
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper)
          .toHaveLength(1);
        expect(wrapper.find("tr"))
          .toHaveLength(4);
      });
    });

    expect(
      wrapper
        .find({ name: "maxAcceptanceDays" })
        .find("input")
        .prop("value"))
      .toBe("");

    expect(
      wrapper
        .find({ name: "maxAcceptanceSeverity" })
        .find("input")
        .prop("value"))
      .toBe("10.0");

    expect(
      wrapper
        .find({ name: "maxNumberAcceptations" })
        .find("input")
        .prop("value"))
      .toBe("");

    expect(
      wrapper
        .find({ name: "minAcceptanceSeverity" })
        .find("input")
        .prop("value"))
      .toBe("0.0");
  });

  it("should render an error message", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [
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
      <MemoryRouter initialEntries={["/orgs/imamura/policies"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route path="/orgs/:organizationName/policies">
              <OrganizationPolicies {...mockProps} />
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(msgError)
          .toHaveBeenCalled();
        expect(wrapper.find("table"))
          .toHaveLength(0);
      });
    });
  });

  it("should update the policies", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [
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
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptations: 5,
              minAcceptanceSeverity: 3,
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
            // tslint:disable-next-line: no-null-keyword
            minAcceptanceSeverity: null,
            organizationId: mockProps.organizationId,
            organizationName: "imamura",
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
              maxAcceptanceDays: 2,
              maxAcceptanceSeverity: 8.9,
              maxNumberAcceptations: 1,
              minAcceptanceSeverity: 0,
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_organization__do_update_organization_policies" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura/policies"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route path="/orgs/:organizationName/policies">
              <authzPermissionsContext.Provider value={mockedPermissions}>
                <OrganizationPolicies {...mockProps} />
              </authzPermissionsContext.Provider>
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper)
          .toHaveLength(1);
        expect(wrapper.find("tr"))
          .toHaveLength(4);
      });
    });

    const form: ReactWrapper = wrapper.find("genericForm");
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
    let saveButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper) => element.contains("Save"))
      .first();

    expect(saveButton)
      .toHaveLength(0);

    maxAcceptanceDays.simulate("change", { target: { value: "2" }});
    maxAcceptanceSeverity.simulate("change", { target: { value: "8.9" }});
    maxNumberAcceptations.simulate("change", { target: { value: "1" }});
    minAcceptanceSeverity.simulate("change", { target: { value: "" } });

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        saveButton = wrapper
          .find("button")
          .filterWhere((element: ReactWrapper) => element.contains("Save"))
          .first();
        expect(saveButton)
          .toHaveLength(1);
      });
    });

    form.simulate("submit");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(msgSuccess)
          .toHaveBeenCalled();
        expect(
          wrapper
            .find({ name: "maxAcceptanceDays" })
            .find("input")
            .prop("value"))
          .toBe("2");
      });
    });
  });

  it("should not show save button", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [
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
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptations: 2,
              minAcceptanceSeverity: 3,
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura/policies"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route path="/orgs/:organizationName/policies">
              <OrganizationPolicies {...mockProps} />
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper)
          .toHaveLength(1);
        expect(wrapper.find("tr"))
          .toHaveLength(4);
      });
    });

    const maxAcceptanceDays: ReactWrapper = wrapper
      .find({ name: "maxAcceptanceDays" })
      .find("input");
    let saveButton: ReactWrapper = wrapper
      .find("button")
      .filterWhere((element: ReactWrapper) => element.contains("Save"))
      .first();

    expect(saveButton)
      .toHaveLength(0);

    maxAcceptanceDays.simulate("change", { target: { value: "2" }});

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        saveButton = wrapper
          .find("button")
          .filterWhere((element: ReactWrapper) => element.contains("Save"))
          .first();
        expect(saveButton)
          .toHaveLength(0);
      });
    });
  });

  it("should handle errors", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [
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
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptations: 2,
              minAcceptanceSeverity: 3,
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
            organizationName: "imamura",
          },
        },
        result: {
          errors: [new GraphQLError("Exception - Acceptance days should be a positive integer")],
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
            organizationName: "imamura",
          },
        },
        result: {
          errors: [new GraphQLError(
            "Exception - Severity value should be a positive floating number between 0.0 a 10.0",
          )],
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
            organizationName: "imamura",
          },
        },
        result: {
          errors: [new GraphQLError(
            "Exception - Min acceptance severity value should not be higher than the max value",
          )],
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
            organizationName: "imamura",
          },
        },
        result: {
          errors: [new GraphQLError("Exception - Number of acceptations should be zero or positive")],
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
            organizationName: "imamura",
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_organization__do_update_organization_policies" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura/policies"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <Route path="/orgs/:organizationName/policies">
              <authzPermissionsContext.Provider value={mockedPermissions}>
                <OrganizationPolicies {...mockProps} />
              </authzPermissionsContext.Provider>
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper)
          .toHaveLength(1);
        expect(wrapper.find("tr"))
          .toHaveLength(4);
      });
    });

    const form: ReactWrapper = wrapper.find("genericForm");
    const maxAcceptanceDays: ReactWrapper = wrapper
      .find({ name: "maxAcceptanceDays" })
      .find("input");

    maxAcceptanceDays.simulate("change", { target: { value: "1" }});
    form.simulate("submit");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(msgError)
          .toBeCalledWith(translate.t("organization.tabs.policies.errors.maxAcceptanceDays"));
      });
    });

    form.simulate("submit");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(msgError)
          .toBeCalledWith(translate.t("organization.tabs.policies.errors.acceptanceSeverity"));
      });
    });

    form.simulate("submit");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(msgError)
          .toBeCalledWith(translate.t("organization.tabs.policies.errors.acceptanceSeverityRange"));
      });
    });

    form.simulate("submit");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(msgError)
          .toBeCalledWith(translate.t("organization.tabs.policies.errors.maxNumberAcceptations"));
      });
    });

    form.simulate("submit");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(msgError)
          .toBeCalledWith(translate.t("group_alerts.error_textsad"));
      });
    });
  });
});
