import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import waitForExpect from "wait-for-expect";

import { AddProjectModal } from "scenes/Dashboard/components/AddProjectModal";
import {
  CREATE_PROJECT_MUTATION,
  PROJECTS_NAME_QUERY,
} from "scenes/Dashboard/components/AddProjectModal/queries";
import { OrganizationGroups } from "scenes/Dashboard/containers/OrganizationGroupsView";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/OrganizationGroupsView/queries";
import type { IOrganizationGroupsProps } from "scenes/Dashboard/containers/OrganizationGroupsView/types";
import store from "store/index";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";

const mockHistoryPush: jest.Mock = jest.fn();

jest.mock(
  "react-router-dom",
  (): Dictionary => {
    const mockedRouter: Dictionary<() => Dictionary> = jest.requireActual(
      "react-router-dom"
    );

    return {
      ...mockedRouter,
      useHistory: (): Dictionary => ({
        ...mockedRouter.useHistory(),
        push: mockHistoryPush,
      }),
    };
  }
);

jest.mock(
  "../../../../utils/notifications",
  (): Dictionary => {
    const mockedNotifications: Dictionary<
      () => Dictionary
    > = jest.requireActual("../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();

    return mockedNotifications;
  }
);

describe("Organization groups view", (): void => {
  const mockProps: IOrganizationGroupsProps = {
    organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationGroups).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              projects: [
                {
                  description: "Continuous type test project",
                  hasDrills: true,
                  hasForces: true,
                  hasIntegrates: true,
                  name: "unittesting",
                  subscription: "continuous",
                  userRole: "customer",
                },
                {
                  description: "One-shot type test project",
                  hasDrills: true,
                  hasForces: false,
                  hasIntegrates: true,
                  name: "oneshottest",
                  subscription: "oneshot",
                  userRole: "customeradmin",
                },
                {
                  description: "Continuous project for deletion",
                  hasDrills: false,
                  hasForces: false,
                  hasIntegrates: false,
                  name: "pendingproject",
                  subscription: "continuous",
                  userRole: "group_manager",
                },
              ],
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_create_group_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route path={"/orgs/:organizationName/groups"}>
              <authzPermissionsContext.Provider value={mockedPermissions}>
                <OrganizationGroups organizationId={mockProps.organizationId} />
              </authzPermissionsContext.Provider>
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
          expect(wrapper.find("tr")).toHaveLength(4);
        });
      }
    );

    const newGroupButton: ReactWrapper = wrapper.find("button").first();
    const oneshottestRow: ReactWrapper = wrapper.find("tr").at(1);
    const pendingProjectRow: ReactWrapper = wrapper.find("tr").at(2);
    const UNIT_TESTING_ROW_AT = 3;
    const unittestingRow: ReactWrapper = wrapper
      .find("tr")
      .at(UNIT_TESTING_ROW_AT);

    expect(newGroupButton.text()).toMatch(/New/u);

    expect(oneshottestRow.text()).toContain("ONESHOTTEST");
    expect(oneshottestRow.text()).toContain("Oneshot");
    expect(oneshottestRow.text()).toContain("User Manager");
    expect(
      oneshottestRow
        .find("span")
        .filterWhere((element: ReactWrapper): boolean =>
          element.contains("Enabled")
        )
    ).toHaveLength(2);
    expect(
      oneshottestRow
        .find("span")
        .filterWhere((element: ReactWrapper): boolean =>
          element.contains("Disabled")
        )
    ).toHaveLength(1);

    const PENDING_PROJECT_ROW_LENGTH = 3;

    expect(pendingProjectRow.text()).toContain("PENDINGPROJECT");
    expect(pendingProjectRow.text()).toContain("Continuous");
    expect(pendingProjectRow.text()).toContain("Group Manager");
    expect(
      pendingProjectRow
        .find("span")
        .filterWhere((element: ReactWrapper): boolean =>
          element.contains("Disabled")
        )
    ).toHaveLength(PENDING_PROJECT_ROW_LENGTH);

    const UNIT_TESTING_ROW_LENGTH = 3;

    expect(unittestingRow.text()).toContain("UNITTESTING");
    expect(unittestingRow.text()).toContain("User");
    expect(unittestingRow.text()).toContain("Continuous");
    expect(
      unittestingRow
        .find("span")
        .filterWhere((element: ReactWrapper): boolean =>
          element.contains("Enabled")
        )
    ).toHaveLength(UNIT_TESTING_ROW_LENGTH);

    unittestingRow.simulate("click");

    expect(mockHistoryPush).toHaveBeenCalledWith(
      "/orgs/okada/groups/unittesting/vulns"
    );
  });

  it("should show an error", async (): Promise<void> => {
    expect.hasAssertions();

    const mockErrors: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mockErrors}>
            <Route path={"/orgs/:organizationName/groups"}>
              <OrganizationGroups organizationId={mockProps.organizationId} />
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          // eslint-disable-next-line jest/prefer-called-with
          expect(msgError).toHaveBeenCalled();
          expect(wrapper.find("table")).toHaveLength(0);
        });
      }
    );
  });

  it("should add a new group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              projects: [
                {
                  description: "Continuous type test project",
                  hasDrills: true,
                  hasForces: true,
                  hasIntegrates: true,
                  name: "unittesting",
                  subscription: "continuous",
                  userRole: "customer",
                },
                {
                  description: "One-shot type test project",
                  hasDrills: true,
                  hasForces: false,
                  hasIntegrates: true,
                  name: "oneshottest",
                  subscription: "oneshot",
                  userRole: "customeradmin",
                },
              ],
            },
          },
        },
      },
      {
        request: {
          query: PROJECTS_NAME_QUERY,
        },
        result: {
          data: {
            internalNames: {
              name: "AKAME",
            },
          },
        },
      },
      {
        request: {
          query: CREATE_PROJECT_MUTATION,
          variables: {
            description: "Test project",
            hasDrills: true,
            hasForces: true,
            organization: "OKADA",
            projectName: "AKAME",
            subscription: "CONTINUOUS",
          },
        },
        result: {
          data: {
            createProject: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          data: {
            organization: {
              projects: [
                {
                  description: "Continuous type test project",
                  hasDrills: true,
                  hasForces: true,
                  hasIntegrates: true,
                  name: "unittesting",
                  subscription: "continuous",
                  userRole: "customer",
                },
                {
                  description: "One-shot type test project",
                  hasDrills: true,
                  hasForces: false,
                  hasIntegrates: true,
                  name: "oneshottest",
                  subscription: "oneshot",
                  userRole: "customeradmin",
                },
                {
                  description: "Test project",
                  hasDrills: true,
                  hasForces: true,
                  hasIntegrates: true,
                  name: "akame",
                  subscription: "continuous",
                  userRole: "customeradmin",
                },
              ],
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_create_group_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route path={"/orgs/:organizationName/groups"}>
              <authzPermissionsContext.Provider value={mockedPermissions}>
                <OrganizationGroups organizationId={mockProps.organizationId} />
              </authzPermissionsContext.Provider>
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );

    const newGroupButton: ReactWrapper = wrapper.find("button").first();
    newGroupButton.simulate("click");

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(
            wrapper
              .find(AddProjectModal)
              .find({ name: "name" })
              .find("input")
              .prop("value")
          ).toBe("AKAME");
        });
      }
    );

    const form: ReactWrapper = wrapper
      .find(AddProjectModal)
      .find("genericForm");
    const descriptionField: ReactWrapper = wrapper
      .find(AddProjectModal)
      .find({ name: "description" })
      .find("input");
    const typeField: ReactWrapper = wrapper
      .find(AddProjectModal)
      .find({ name: "type" })
      .find("select");

    descriptionField.simulate("change", { target: { value: "Test project" } });
    typeField.simulate("change", { target: { value: "CONTINUOUS" } });
    form.simulate("submit");

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper.find("tr")).toHaveLength(4);
        });
      }
    );
  });
});
