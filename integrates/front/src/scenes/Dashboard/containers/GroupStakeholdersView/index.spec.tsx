import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { DataTableNext } from "components/DataTableNext";
import { timeFromNow } from "components/DataTableNext/formatters";
import type { ITableProps } from "components/DataTableNext/types";
import { GroupStakeholdersView } from "scenes/Dashboard/containers/GroupStakeholdersView";
import {
  ADD_STAKEHOLDER_MUTATION,
  GET_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
  UPDATE_GROUP_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/GroupStakeholdersView/queries";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary = jest.requireActual(
    "../../../../utils/notifications"
  );
  mockedNotifications.msgSuccess = jest.fn(); // eslint-disable-line fp/no-mutation, jest/prefer-spy-on
  mockedNotifications.msgError = jest.fn(); // eslint-disable-line fp/no-mutation, jest/prefer-spy-on

  return mockedNotifications;
});

/*
 * Important Notice: When going from redux-form to Formik, some of the changes to keep
 * in mind is that to simulate a change event you now must provide the name of the field
 * along with the value to let Formik know which field should be changed. As seen in
 * https://github.com/formium/formik/issues/481#issuecomment-374970940
 */

describe("Group stakeholders view", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_STAKEHOLDERS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            name: "TEST",
            stakeholders: [
              {
                email: "user@gmail.com",
                firstLogin: "2017-09-05 15:00:00",
                invitationState: "CONFIRMED",
                lastLogin: "2017-10-29 13:40:37",
                phoneNumber: "+573123210121",
                responsibility: "Test responsibility",
                role: "customer",
              },
            ],
          },
        },
      },
    },
    {
      request: {
        query: GET_STAKEHOLDERS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            name: "TEST",
            stakeholders: [
              {
                email: "user@gmail.com",
                firstLogin: "2017-09-05 15:00:00",
                invitationState: "CONFIRMED",
                lastLogin: "2017-10-29 13:40:37",
                phoneNumber: "+573123210121",
                responsibility: "Rest responsibility",
                role: "customer",
              },
              {
                email: "unittest@test.com",
                firstLogin: "2017-09-05 15:00:00",
                invitationState: "CONFIRMED",
                lastLogin: "2017-10-29 13:40:37",
                phoneNumber: "+573123210123",
                responsibility: "Project Manager",
                role: "hacker",
              },
            ],
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_STAKEHOLDERS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupStakeholdersView).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mockError}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);

    jest.clearAllMocks();
  });

  it("should display all group stakeholder columns", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const stakeholderTable: ReactWrapper<ITableProps> = wrapper
      .find(DataTableNext)
      .filter({ id: "tblUsers" });

    const tableHeader: ReactWrapper = stakeholderTable.find("Header");

    expect(tableHeader.text()).toContain("Stakeholder email");
    expect(tableHeader.text()).toContain("Role");
    expect(tableHeader.text()).toContain("Responsibility");
    expect(tableHeader.text()).toContain("Phone Number");
    expect(tableHeader.text()).toContain("First login");
    expect(tableHeader.text()).toContain("Last login");
    expect(tableHeader.text()).toContain("Invitation");

    const firstRow: ReactWrapper = stakeholderTable.find("RowAggregator");

    expect(firstRow.text()).toContain("user@gmail.com");
    expect(firstRow.text()).toContain("User");
    expect(firstRow.text()).toContain("Test responsibility");
    expect(firstRow.text()).toContain("+573123210121");
    expect(firstRow.text()).toContain("2017-09-05 15:00:00");
    expect(firstRow.text()).toContain(timeFromNow("2017-10-29 13:40:37"));
    expect(firstRow.text()).toContain("Confirmed");

    jest.clearAllMocks();
  });

  it("should render an add stakeholder component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);

    jest.clearAllMocks();
  });

  it("should render an edit stakeholder component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <Route
              component={GroupStakeholdersView}
              path={"/groups/:groupName/stakeholders"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);

    jest.clearAllMocks();
  });

  it("should open a modal to add stakeholder", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_grant_stakeholder_access_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupStakeholdersView}
                path={"/groups/:groupName/stakeholders"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const addUserModal: ReactWrapper = wrapper
      .find("ModalBase")
      .find({ headerTitle: "Add stakeholder to this group", open: true });

    expect(addUserModal).toHaveLength(0);

    await act(async (): Promise<void> => {
      const addButton: ReactWrapper = wrapper
        .find("button")
        .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
        .at(0);
      addButton.simulate("click");

      await wait(0);
      wrapper.update();
    });
    const addUserModal2: ReactWrapper = wrapper
      .find("ModalBase")
      .find({ headerTitle: "Add stakeholder to this group", open: true });

    expect(addUserModal2).toHaveLength(1);

    jest.clearAllMocks();
  });

  it("should open a modal to edit stakeholder", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_group_stakeholder_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mocks}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupStakeholdersView}
                path={"/groups/:groupName/stakeholders"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const editUserModal: ReactWrapper = wrapper
      .find("ModalBase")
      .find({ headerTitle: "Edit stakeholder information", open: true });

    expect(editUserModal).toHaveLength(0);

    const userInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("user@gmail.com")
      )
      .at(0);
    userInfo.simulate("click");
    const addButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Edit"))
      .at(0);
    addButton.simulate("click");
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const editUserModal2: ReactWrapper = wrapper
      .find("ModalBase")
      .find({ headerTitle: "Edit stakeholder information", open: true });

    expect(editUserModal2).toHaveLength(1);

    jest.clearAllMocks();
  });

  it("should add stakeholder to the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_STAKEHOLDER_MUTATION,
          variables: {
            email: "unittest@test.com",
            groupName: "TEST",
            phoneNumber: "+573123210123",
            responsibility: "Project Manager",
            role: "HACKER",
          },
        },
        result: {
          data: {
            grantStakeholderAccess: {
              grantedStakeholder: {
                email: "unittest@test.com",
              },
              success: true,
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_grant_stakeholder_access_mutate" },
      { action: "grant_group_level_role:hacker" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider
            addTypename={false}
            mocks={mocks.concat(mocksMutation)}
          >
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupStakeholdersView}
                path={"/groups/:groupName/stakeholders"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const addButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addUserModal: ReactWrapper = wrapper
      .find("ModalBase")
      .find({ headerTitle: "Add stakeholder to this group", open: true });

    expect(addUserModal).toHaveLength(1);

    const emailInput: ReactWrapper = addUserModal
      .find({ name: "email", type: "text" })
      .at(0)
      .find("input");
    emailInput.simulate("change", {
      target: { name: "email", value: "unittest@test.com" },
    });
    const phoneNumberInput: ReactWrapper = addUserModal
      .find({ name: "phoneNumber", type: "text" })
      .at(0)
      .find("input");
    phoneNumberInput.simulate("change", {
      target: { name: "phoneNumber", value: "+573123210123" },
    });
    const responsibilityInput: ReactWrapper = addUserModal
      .find({ name: "responsibility", type: "text" })
      .at(0)
      .find("input");
    responsibilityInput.simulate("change", {
      target: { name: "responsibility", value: "Project Manager" },
    });
    const select: ReactWrapper = addUserModal
      .find("select")
      .findWhere((element: ReactWrapper): boolean => element.contains("Hacker"))
      .at(0);
    select.simulate("change", { target: { name: "role", value: "HACKER" } });
    const form: ReactWrapper = addUserModal.find("Formik").at(0);
    await act(async (): Promise<void> => {
      form.simulate("submit");

      await wait(0);
      wrapper.update();
    });

    const addUserModal2: ReactWrapper = wrapper
      .find("ModalBase")
      .find({ headerTitle: "Add stakeholder to this group", open: true });

    expect(addUserModal2).toHaveLength(0);

    await wait(0);

    expect(msgSuccess).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });

  it("should remove stakeholder from the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_STAKEHOLDER_MUTATION,
          variables: {
            groupName: "TEST",
            userEmail: "user@gmail.com",
          },
        },
        result: {
          data: {
            removeStakeholderAccess: {
              removedEmail: "user@gmail.com",
              success: true,
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_stakeholder_access_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider
            addTypename={false}
            mocks={mocks.concat(mocksMutation)}
          >
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupStakeholdersView}
                path={"/groups/:groupName/stakeholders"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const userInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("user@gmail.com")
      )
      .at(0);
    userInfo.simulate("click");
    const removeButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Remove"))
      .at(0);
    await act(async (): Promise<void> => {
      removeButton.simulate("click");

      await wait(0);
      wrapper.update();
    });

    await wait(0);

    expect(msgSuccess).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });

  it("should edit stakeholder from the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: UPDATE_GROUP_STAKEHOLDER_MUTATION,
          variables: {
            email: "user@gmail.com",
            groupName: "TEST",
            phoneNumber: "+573123210123",
            responsibility: "Project Manager",
            role: "HACKER",
          },
        },
        result: {
          data: {
            updateGroupStakeholder: {
              modifiedStakeholder: {
                email: "user@gmail.com",
              },
              success: true,
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_group_stakeholder_mutate" },
      { action: "grant_group_level_role:hacker" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider
            addTypename={false}
            mocks={mocks.concat(mocksMutation)}
          >
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupStakeholdersView}
                path={"/groups/:groupName/stakeholders"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const userInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("user@gmail.com")
      )
      .at(0);
    userInfo.simulate("click");
    const editButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Edit"))
      .at(0);
    editButton.simulate("click");
    const editUserModal: ReactWrapper = wrapper
      .find("ModalBase")
      .find({ headerTitle: "Edit stakeholder information", open: true });

    expect(editUserModal).toHaveLength(1);

    const phoneNumberInput: ReactWrapper = editUserModal
      .find({ name: "phoneNumber", type: "text" })
      .at(0)
      .find("input");
    phoneNumberInput.simulate("change", {
      target: { name: "phoneNumber", value: "+573123210123" },
    });
    const responsibilityInput: ReactWrapper = editUserModal
      .find({ name: "responsibility", type: "text" })
      .at(0)
      .find("input");
    responsibilityInput.simulate("change", {
      target: { name: "responsibility", value: "Project Manager" },
    });
    const select: ReactWrapper = editUserModal
      .find("select")
      .findWhere((element: ReactWrapper): boolean => element.contains("Hacker"))
      .at(0);
    select.simulate("change", { target: { name: "role", value: "HACKER" } });
    const form: ReactWrapper = editUserModal.find("Formik").at(0);
    await act(async (): Promise<void> => {
      form.simulate("submit");

      await wait(0);
      wrapper.update();
    });
    const editUserModal2: ReactWrapper = wrapper
      .find("ModalBase")
      .find({ headerTitle: "Edit stakeholder information", open: true });

    expect(editUserModal2).toHaveLength(0);

    await wait(0);

    expect(msgSuccess).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });

  it("should handle errors when adding a stakeholder to the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_STAKEHOLDER_MUTATION,
          variables: {
            email: "unittest@test.com",
            groupName: "TEST",
            phoneNumber: "+573123210123",
            responsibility: "Project Manager",
            role: "HACKER",
          },
        },
        result: {
          errors: [
            new GraphQLError("Access denied"),
            new GraphQLError("Exception - Email is not valid"),
            new GraphQLError("Exception - Invalid field in form"),
            new GraphQLError("Exception - Invalid characters"),
            new GraphQLError("Exception - Invalid phone number in form"),
            new GraphQLError("Exception - Invalid email address in form"),
            new GraphQLError(
              "Exception - Groups without an active Fluid Attacks service " +
                "can not have Fluid Attacks staff"
            ),
            new GraphQLError(
              "Exception - Groups with any active Fluid Attacks service " +
                "can only have Hackers provided by Fluid Attacks"
            ),
          ],
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_grant_stakeholder_access_mutate" },
      { action: "grant_group_level_role:hacker" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider
            addTypename={false}
            mocks={mocks.concat(mocksMutation)}
          >
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupStakeholdersView}
                path={"/groups/:groupName/stakeholders"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const addButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addUserModal: ReactWrapper = wrapper
      .find("ModalBase")
      .find({ headerTitle: "Add stakeholder to this group", open: true });

    expect(addUserModal).toHaveLength(1);

    const emailInput: ReactWrapper = addUserModal
      .find({ name: "email", type: "text" })
      .at(0)
      .find("input");
    emailInput.simulate("change", {
      target: { name: "email", value: "unittest@test.com" },
    });
    const phoneNumberInput: ReactWrapper = addUserModal
      .find({ name: "phoneNumber", type: "text" })
      .at(0)
      .find("input");
    phoneNumberInput.simulate("change", {
      target: { name: "phoneNumber", value: "+573123210123" },
    });
    const responsibilityInput: ReactWrapper = addUserModal
      .find({ name: "responsibility", type: "text" })
      .at(0)
      .find("input");
    responsibilityInput.simulate("change", {
      target: { name: "responsibility", value: "Project Manager" },
    });
    const select: ReactWrapper = addUserModal
      .find("select")
      .findWhere((element: ReactWrapper): boolean => element.contains("Hacker"))
      .at(0);
    select.simulate("change", { target: { name: "role", value: "HACKER" } });
    const form: ReactWrapper = addUserModal.find("Formik").at(0);
    await act(async (): Promise<void> => {
      form.simulate("submit");

      await wait(0);
      wrapper.update();
    });
    const addUserModal2: ReactWrapper = wrapper
      .find("ModalBase")
      .find({ headerTitle: "Add stakeholder to this group", open: true });

    const TEST_TIMES_CALLED = 8;

    expect(addUserModal2).toHaveLength(0);

    await wait(0);

    expect(msgError).toHaveBeenCalledTimes(TEST_TIMES_CALLED);

    jest.clearAllMocks();
  });

  it("should handle error when removing a stakeholder from the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_STAKEHOLDER_MUTATION,
          variables: {
            groupName: "TEST",
            userEmail: "user@gmail.com",
          },
        },
        result: { errors: [new GraphQLError("Access denied")] },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_stakeholder_access_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider
            addTypename={false}
            mocks={mocks.concat(mocksMutation)}
          >
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupStakeholdersView}
                path={"/groups/:groupName/stakeholders"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const userInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("user@gmail.com")
      )
      .at(0);
    userInfo.simulate("click");
    const removeButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Remove"))
      .at(0);
    await act(async (): Promise<void> => {
      removeButton.simulate("click");

      await wait(0);
      wrapper.update();
    });
    await wait(0);

    expect(msgError).toHaveBeenCalled(); // eslint-disable-line jest/prefer-called-with

    jest.clearAllMocks();
  });

  it("should handle error when editing a stakeholder from the group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: UPDATE_GROUP_STAKEHOLDER_MUTATION,
          variables: {
            email: "user@gmail.com",
            groupName: "TEST",
            phoneNumber: "+573123210123",
            responsibility: "Project Manager",
            role: "HACKER",
          },
        },
        result: {
          errors: [
            new GraphQLError("Access denied"),
            new GraphQLError("Exception - Invalid field in form"),
            new GraphQLError("Exception - Invalid characters"),
            new GraphQLError("Exception - Invalid phone number in form"),
            new GraphQLError(
              "Exception - Groups without an active Fluid Attacks service " +
                "can not have Fluid Attacks staff"
            ),
            new GraphQLError(
              "Exception - Groups with any active Fluid Attacks service " +
                "can only have Hackers provided by Fluid Attacks"
            ),
          ],
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_group_stakeholder_mutate" },
      { action: "grant_group_level_role:hacker" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/stakeholders"]}>
        <Provider store={store}>
          <MockedProvider
            addTypename={false}
            mocks={mocks.concat(mocksMutation)}
          >
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupStakeholdersView}
                path={"/groups/:groupName/stakeholders"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const userInfo: ReactWrapper = wrapper
      .find("tr")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("user@gmail.com")
      )
      .at(0);
    userInfo.simulate("click");
    const editButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Edit"))
      .at(0);
    editButton.simulate("click");
    const editUserModal: ReactWrapper = wrapper.find("ModalBase").find({
      headerTitle: "Edit stakeholder information",
      open: true,
    });

    expect(editUserModal).toHaveLength(1);

    const phoneNumberInput: ReactWrapper = editUserModal
      .find({ name: "phoneNumber", type: "text" })
      .at(0)
      .find("input");
    phoneNumberInput.simulate("change", {
      target: { name: "phoneNumber", value: "+573123210123" },
    });
    const responsibilityInput: ReactWrapper = editUserModal
      .find({ name: "responsibility", type: "text" })
      .at(0)
      .find("input");
    responsibilityInput.simulate("change", {
      target: { name: "responsibility", value: "Project Manager" },
    });
    const select: ReactWrapper = editUserModal
      .find("select")
      .findWhere((element: ReactWrapper): boolean => element.contains("Hacker"))
      .at(0);
    select.simulate("change", { target: { name: "role", value: "HACKER" } });
    const form: ReactWrapper = editUserModal.find("Formik").at(0);
    await act(async (): Promise<void> => {
      form.simulate("submit");

      await wait(0);
      wrapper.update();
    });
    const editUserModal2: ReactWrapper = wrapper.find("ModalBase").find({
      headerTitle: "Edit stakeholder information",
      open: true,
    });

    const TEST_TIMES_CALLED = 6;

    expect(editUserModal2).toHaveLength(0);

    await wait(0);

    expect(msgError).toHaveBeenCalledTimes(TEST_TIMES_CALLED);

    jest.clearAllMocks();
  });
});
