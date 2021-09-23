// Needed to test Formik components
/* eslint-disable @typescript-eslint/no-empty-function, @typescript-eslint/no-unsafe-return */
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";
import {
  ADD_GROUP_MUTATION,
  GROUPS_NAME_QUERY,
} from "scenes/Dashboard/components/AddGroupModal/queries";
import { OrganizationGroups } from "scenes/Dashboard/containers/OrganizationGroupsView";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/OrganizationGroupsView/queries";
import type { IOrganizationGroupsProps } from "scenes/Dashboard/containers/OrganizationGroupsView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";

const mockHistoryPush: jest.Mock = jest.fn();

jest.mock("react-router-dom", (): Dictionary => {
  const mockedRouter: Dictionary<() => Dictionary> =
    jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Dictionary => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

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
              groups: [
                {
                  description: "Continuous type test group",
                  hasMachine: true,
                  hasSquad: true,
                  name: "unittesting",
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "customer",
                },
                {
                  description: "One-shot type test group",
                  hasMachine: true,
                  hasSquad: true,
                  name: "oneshottest",
                  service: "WHITE",
                  subscription: "oneshot",
                  userRole: "customeradmin",
                },
                {
                  description: "Continuous group for deletion",
                  hasMachine: true,
                  hasSquad: false,
                  name: "pendingGroup",
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "system_owner",
                },
              ],
              name: "okada",
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_group_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/groups"}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <OrganizationGroups organizationId={mockProps.organizationId} />
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("tr")).toHaveLength(4);
      });
    });

    const newGroupButton: ReactWrapper = wrapper.find("button").first();
    const oneshottestRow: ReactWrapper = wrapper.find("tr").at(1);
    const pendingGroupRow: ReactWrapper = wrapper.find("tr").at(2);
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
        .find({ className: "v-mid" })
        .filterWhere((element: ReactWrapper): boolean =>
          element.contains("Enabled")
        )
    ).toHaveLength(2);
    expect(
      oneshottestRow
        .find({ className: "v-mid" })
        .filterWhere((element: ReactWrapper): boolean =>
          element.contains("Disabled")
        )
    ).toHaveLength(0);

    const PENDING_GROUP_ROW_LENGTH = 1;

    expect(pendingGroupRow.text()).toContain("PENDINGGROUP");
    expect(pendingGroupRow.text()).toContain("Continuous");
    expect(pendingGroupRow.text()).toContain("System Owner");
    expect(
      pendingGroupRow
        .find({ className: "v-mid" })
        .filterWhere((element: ReactWrapper): boolean =>
          element.contains("Disabled")
        )
    ).toHaveLength(PENDING_GROUP_ROW_LENGTH);

    const UNIT_TESTING_ROW_LENGTH = 2;

    expect(unittestingRow.text()).toContain("UNITTESTING");
    expect(unittestingRow.text()).toContain("User");
    expect(unittestingRow.text()).toContain("Continuous");
    expect(
      unittestingRow
        .find({ className: "v-mid" })
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
        <MockedProvider addTypename={false} mocks={mockErrors}>
          <Route path={"/orgs/:organizationName/groups"}>
            <OrganizationGroups organizationId={mockProps.organizationId} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        // eslint-disable-next-line jest/prefer-called-with
        expect(msgError).toHaveBeenCalled();
        expect(wrapper.find("table")).toHaveLength(0);
      });
    });
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
              groups: [
                {
                  description: "Continuous type test group",
                  hasMachine: true,
                  hasSquad: true,
                  name: "unittesting",
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "customer",
                },
                {
                  description: "One-shot type test group",
                  hasMachine: true,
                  hasSquad: true,
                  name: "oneshottest",
                  service: "WHITE",
                  subscription: "oneshot",
                  userRole: "customeradmin",
                },
              ],
              name: "okada",
            },
          },
        },
      },
      {
        request: {
          query: GROUPS_NAME_QUERY,
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
          query: ADD_GROUP_MUTATION,
          variables: {
            description: "Test group",
            groupName: "AKAME",
            hasForces: true,
            hasSquad: true,
            organization: "OKADA",
            subscription: "CONTINUOUS",
          },
        },
        result: {
          data: {
            addGroup: {
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
              groups: [
                {
                  description: "Continuous type test group",
                  hasAsm: true,
                  hasForces: true,
                  hasSquad: true,
                  name: "unittesting",
                  subscription: "continuous",
                  userRole: "customer",
                },
                {
                  description: "One-shot type test group",
                  hasAsm: true,
                  hasForces: false,
                  hasSquad: true,
                  name: "oneshottest",
                  subscription: "oneshot",
                  userRole: "customeradmin",
                },
                {
                  description: "Test group",
                  hasAsm: true,
                  hasForces: true,
                  hasSquad: true,
                  name: "akame",
                  subscription: "continuous",
                  userRole: "customeradmin",
                },
              ],
              name: "okada",
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_group_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/groups"}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <OrganizationGroups organizationId={mockProps.organizationId} />
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );
    const newGroupButton = (): ReactWrapper => wrapper.find("button").first();
    newGroupButton().simulate("click");

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(
          wrapper
            .find(AddGroupModal)
            .find({ name: "name" })
            .find("input")
            .prop("value")
        ).toBe("AKAME");
      });
    });

    const form = (): ReactWrapper => wrapper.find(AddGroupModal).find("Formik");
    const descriptionField = (): ReactWrapper =>
      wrapper.find(AddGroupModal).find({ name: "description" }).find("input");
    const typeField = (): ReactWrapper =>
      wrapper.find(AddGroupModal).find({ name: "type" }).find("select");

    descriptionField().simulate("change", {
      target: { name: "description", value: "Test group" },
    });
    typeField().simulate("change", {
      target: { name: "type", value: "CONTINUOUS" },
    });
    form().simulate("submit");

    await act(async (): Promise<void> => {
      wrapper.update();
      const delay = 50;
      await wait(delay);
    });

    const finalGroupQuantity = 3;

    expect(wrapper.find("tr")).toHaveLength(finalGroupQuantity);
  });
});
