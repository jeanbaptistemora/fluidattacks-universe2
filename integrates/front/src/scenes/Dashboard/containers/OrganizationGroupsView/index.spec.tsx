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

import { AddProjectModal } from "scenes/Dashboard/components/AddProjectModal";
import { CREATE_PROJECT_MUTATION, PROJECTS_NAME_QUERY } from "scenes/Dashboard/components/AddProjectModal/queries";
import { OrganizationGroups } from "scenes/Dashboard/containers/OrganizationGroupsView";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/OrganizationGroupsView/queries";
import { IOrganizationGroupsProps } from "scenes/Dashboard/containers/OrganizationGroupsView/types";
import store from "store/index";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";

const mockHistoryPush: jest.Mock = jest.fn();

jest.mock("react-router-dom", (): Dictionary => {
  const mockedRouter: Dictionary<() => Dictionary> = jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Dictionary => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual("../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();

  return mockedNotifications;
});

describe("Organization groups view", () => {
  const mockProps: IOrganizationGroupsProps = {
    organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
  };

  it("should return a function", () => {
    expect(typeof OrganizationGroups)
      .toEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    const mocks: ReadonlyArray<MockedResponse> = [
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
      { action: "backend_api_resolvers_project__do_create_project" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura/groups"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false} >
            <Route path="/orgs/:organizationName/groups">
              <authzPermissionsContext.Provider value={mockedPermissions}>
                <OrganizationGroups {...mockProps} />
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

    const newGroupButton: ReactWrapper = wrapper
      .find("button")
      .first();
    const oneshottestRow: ReactWrapper = wrapper
      .find("tr")
      .at(1);
    const pendingProjectRow: ReactWrapper = wrapper
      .find("tr")
      .at(2);
    const unittestingRow: ReactWrapper = wrapper
      .find("tr")
      .at(3);

    expect(newGroupButton.text())
      .toMatch(/New/);

    expect(oneshottestRow.text())
      .toContain("ONESHOTTEST");
    expect(oneshottestRow.text())
      .toContain("Oneshot");
    expect(oneshottestRow.text())
      .toContain("User Manager");
    expect(
        oneshottestRow
          .find("span")
          .filterWhere((element: ReactWrapper) => element.contains("Enabled")))
      .toHaveLength(2);
    expect(
        oneshottestRow
          .find("span")
          .filterWhere((element: ReactWrapper) => element.contains("Disabled")))
      .toHaveLength(1);

    expect(pendingProjectRow.text())
      .toContain("PENDINGPROJECT");
    expect(pendingProjectRow.text())
      .toContain("Continuous");
    expect(pendingProjectRow.text())
      .toContain("Group Manager");
    expect(
      pendingProjectRow
          .find("span")
          .filterWhere((element: ReactWrapper) => element.contains("Disabled")))
      .toHaveLength(3);

    expect(unittestingRow.text())
      .toContain("UNITTESTING");
    expect(unittestingRow.text())
      .toContain("User");
    expect(unittestingRow.text())
        .toContain("Continuous");
    expect(
        unittestingRow
          .find("span")
          .filterWhere((element: ReactWrapper) => element.contains("Enabled")))
      .toHaveLength(3);

    unittestingRow.simulate("click");
    expect(mockHistoryPush)
      .toBeCalledWith("/orgs/imamura/groups/unittesting/");
  });

  it("should show an error", async (): Promise<void> => {
    const mockErrors: ReadonlyArray<MockedResponse> = [
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
      <MemoryRouter initialEntries={["/orgs/imamura/groups"]}>
        <Provider store={store}>
          <MockedProvider mocks={mockErrors} addTypename={false} >
            <Route path="/orgs/:organizationName/groups">
              <OrganizationGroups {...mockProps} />
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

  it("should add a new group", async (): Promise<void> => {
    const mocks: ReadonlyArray<MockedResponse> = [
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
            organization: "IMAMURA",
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
      { action: "backend_api_resolvers_project__do_create_project" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura/groups"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false} >
            <Route path="/orgs/:organizationName/groups">
              <authzPermissionsContext.Provider value={mockedPermissions}>
                <OrganizationGroups {...mockProps} />
              </authzPermissionsContext.Provider>
            </Route>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(
          wrapper
            .find(AddProjectModal)
            .prop("isOpen"))
          .toBe(false);
      });
    });

    const newGroupButton: ReactWrapper = wrapper
      .find("button")
      .first();
    newGroupButton.simulate("click");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(
          wrapper
            .find(AddProjectModal)
            .prop("isOpen"))
          .toBe(true);

        expect(
          wrapper
            .find(AddProjectModal)
            .find({ name: "name" })
            .find("input")
            .prop("value"))
          .toBe("AKAME");
      });
    });

    const form: ReactWrapper = wrapper
      .find(AddProjectModal)
      .find("genericForm");
    const descriptionField: ReactWrapper = wrapper
      .find(AddProjectModal)
      .find({name: "description"})
      .find("input");
    const typeField: ReactWrapper = wrapper
      .find(AddProjectModal)
      .find({name: "type"})
      .find("select");

    descriptionField.simulate("change", { target: { value: "Test project" } });
    typeField.simulate("change", { target: { value: "CONTINUOUS" } });
    form.simulate("submit");

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(
          wrapper
            .find(AddProjectModal)
            .prop("isOpen"))
          .toBe(false);

        expect(wrapper.find("tr"))
        .toHaveLength(4);
      });
    });
  });
});
