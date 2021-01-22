import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { DataTableNext } from "components/DataTableNext";
import { timeFromNow } from "components/DataTableNext/formatters";
import { ITableProps } from "components/DataTableNext/types";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";

import { ProjectStakeholdersView } from "scenes/Dashboard/containers/ProjectStakeholdersView";
import {
  ADD_STAKEHOLDER_MUTATION,
  EDIT_STAKEHOLDER_MUTATION,
  GET_STAKEHOLDERS,
  REMOVE_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/containers/ProjectStakeholdersView/queries";
import { IProjectStakeholdersViewProps } from "scenes/Dashboard/containers/ProjectStakeholdersView/types";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../utils/notifications");
  mockedNotifications.msgSuccess = jest.fn();
  mockedNotifications.msgError = jest.fn();

  return mockedNotifications;
});

describe("Project users view", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  const mockProps: IProjectStakeholdersViewProps = {
    history: {
      action: "PUSH",
      block: (): (() => void) => (): void => undefined,
      createHref: (): string => "",
      go: (): void => undefined,
      goBack: (): void => undefined,
      goForward: (): void => undefined,
      length: 1,
      listen: (): (() => void) => (): void => undefined,
      location: { hash: "", pathname: "/", search: "", state: {} },
      push: (): void => undefined,
      replace: (): void => undefined,
    },
    location: { hash: "", pathname: "/", search: "", state: {} },
    match: {
      isExact: true,
      params: { projectName: "TEST" },
      path: "/",
      url: "",
    },
  };

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_STAKEHOLDERS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            stakeholders: [{
              email: "user@gmail.com",
              firstLogin: "2017-09-05 15:00:00",
              invitationState: "CONFIRMED",
              lastLogin: "2017-10-29 13:40:37",
              phoneNumber: "+573123210121",
              responsibility: "Test responsibility",
              role: "customer",
            }],
          },
        },
      },
    },
    {
      request: {
        query: GET_STAKEHOLDERS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
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
                role: "analyst",
              },
            ],
          },
        },
      },
    },
  ];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_STAKEHOLDERS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (ProjectStakeholdersView))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={false}>
          <ProjectStakeholdersView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should display all group stakeholder columns", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectStakeholdersView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      },
    );

    const stakeholderTable: ReactWrapper<ITableProps> = wrapper
      .find(DataTableNext)
      .filter({ id: "tblUsers" });

    const tableHeader: ReactWrapper = stakeholderTable.find("Header");

    expect(tableHeader.text())
      .toContain("Stakeholder email");
    expect(tableHeader.text())
      .toContain("Role");
    expect(tableHeader.text())
      .toContain("Responsibility");
    expect(tableHeader.text())
      .toContain("Phone Number");
    expect(tableHeader.text())
      .toContain("First login");
    expect(tableHeader.text())
      .toContain("Last login");
    expect(tableHeader.text())
      .toContain("Invitation");

    const firstRow: ReactWrapper = stakeholderTable.find("RowAggregator");

    expect(firstRow.text())
      .toContain("user@gmail.com");
    expect(firstRow.text())
      .toContain("User");
    expect(firstRow.text())
      .toContain("Test responsibility");
    expect(firstRow.text())
      .toContain("+573123210121");
    expect(firstRow.text())
      .toContain("2017-09-05 15:00:00");
    expect(firstRow.text())
      .toContain(timeFromNow("2017-10-29 13:40:37"));
    expect(firstRow.text())
      .toContain("Confirmed");
  });

  it("should render an add stakeholder component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectStakeholdersView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an edit stakeholder component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectStakeholdersView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should open a modal to add stakeholder", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_grant_stakeholder_access_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <ProjectStakeholdersView {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    let addUserModal: ReactWrapper = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Add stakeholder to this group"});
    expect(addUserModal)
      .toHaveLength(0);
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    await act(async () => { await wait(0); wrapper.update(); });
    addUserModal = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Add stakeholder to this group"});
    expect(addUserModal)
      .toHaveLength(1);
  });

  it("should open a modal to edit stakeholder", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_edit_stakeholder_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <ProjectStakeholdersView {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    let editUserModal: ReactWrapper = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Edit stakeholder information"});
    expect(editUserModal)
      .toHaveLength(0);
    const userInfo: ReactWrapper = wrapper.find("tr")
      .findWhere((element: ReactWrapper) => element.contains("user@gmail.com"))
      .at(0);
    userInfo.simulate("click");
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Edit"))
      .at(0);
    addButton.simulate("click");
    await act(async () => { await wait(0); wrapper.update(); });
    editUserModal = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Edit stakeholder information"});
    expect(editUserModal)
      .toHaveLength(1);
  });

  it("should add stakeholder to the project", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: ADD_STAKEHOLDER_MUTATION,
        variables: {
          email: "unittest@test.com",
          phoneNumber: "+573123210123",
          projectName: "TEST",
          responsibility: "Project Manager",
          role: "ANALYST",
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
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_grant_stakeholder_access_mutate" },
      { action: "grant_group_level_role:analyst" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <ProjectStakeholdersView {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    let addUserModal: ReactWrapper = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Add stakeholder to this group"});
    expect(addUserModal)
      .toHaveLength(1);
    const emailInput: ReactWrapper = addUserModal
      .find({name: "email", type: "text"})
      .at(0)
      .find("input");
    emailInput.simulate("change", { target: { value: "unittest@test.com" } });
    const phoneNumberInput: ReactWrapper = addUserModal
      .find({name: "phoneNumber", type: "text"})
      .at(0)
      .find("input");
    phoneNumberInput.simulate("change", { target: { value: "+573123210123" } });
    const responsibilityInput: ReactWrapper = addUserModal
      .find({name: "responsibility", type: "text"})
      .at(0)
      .find("input");
    responsibilityInput.simulate("change", { target: { value: "Project Manager" } });
    const select: ReactWrapper = addUserModal.find("select")
      .findWhere((element: ReactWrapper) => element.contains("Analyst"))
      .at(0);
    select.simulate("change", { target: { value: "ANALYST" } });
    const form: ReactWrapper = addUserModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    addUserModal = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Add stakeholder to this group"});
    expect(addUserModal)
      .toHaveLength(0);
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should remove stakeholder from the project", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: REMOVE_STAKEHOLDER_MUTATION,
        variables: {
          projectName: "TEST",
          userEmail: "user@gmail.com",
        },
      },
      result: { data: { removeStakeholderAccess : { success: true, removedEmail: "user@gmail.com" } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_remove_stakeholder_access_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <ProjectStakeholdersView {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const userInfo: ReactWrapper = wrapper.find("tr")
      .findWhere((element: ReactWrapper) => element.contains("user@gmail.com"))
      .at(0);
    userInfo.simulate("click");
    const removeButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Remove"))
      .at(0);
    removeButton.simulate("click");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should edit stakeholder from the project", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: EDIT_STAKEHOLDER_MUTATION,
        variables: {
          email: "user@gmail.com",
          phoneNumber: "+573123210123",
          projectName: "TEST",
          responsibility: "Project Manager",
          role: "ANALYST",
        },
      },
      result: { data: { editStakeholder : { success: true } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_edit_stakeholder_mutate" },
      { action: "grant_group_level_role:analyst" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <ProjectStakeholdersView {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const userInfo: ReactWrapper = wrapper.find("tr")
      .findWhere((element: ReactWrapper) => element.contains("user@gmail.com"))
      .at(0);
    userInfo.simulate("click");
    const editButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Edit"))
      .at(0);
    editButton.simulate("click");
    let editUserModal: ReactWrapper = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Edit stakeholder information"});
    expect(editUserModal)
      .toHaveLength(1);
    const phoneNumberInput: ReactWrapper = editUserModal
      .find({name: "phoneNumber", type: "text"})
      .at(0)
      .find("input");
    phoneNumberInput.simulate("change", { target: { value: "+573123210123" } });
    const responsibilityInput: ReactWrapper = editUserModal
      .find({name: "responsibility", type: "text"})
      .at(0)
      .find("input");
    responsibilityInput.simulate("change", { target: { value: "Project Manager" } });
    const select: ReactWrapper = editUserModal.find("select")
      .findWhere((element: ReactWrapper) => element.contains("Analyst"))
      .at(0);
    select.simulate("change", { target: { value: "ANALYST" } });
    const form: ReactWrapper = editUserModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    editUserModal = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Edit stakeholder information"});
    expect(editUserModal)
      .toHaveLength(0);
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should handle errors when add stakeholder to the project", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: ADD_STAKEHOLDER_MUTATION,
        variables: {
          email: "unittest@test.com",
          phoneNumber: "+573123210123",
          projectName: "TEST",
          responsibility: "Project Manager",
          role: "ANALYST",
        },
      },
      result: { errors: [
        new GraphQLError("Access denied"),
        new GraphQLError("Exception - Email is not valid"),
        new GraphQLError("Exception - Invalid field in form"),
        new GraphQLError("Exception - Invalid characters"),
        new GraphQLError("Exception - Invalid phone number in form"),
        new GraphQLError("Exception - Invalid email address in form"),
        new GraphQLError("Exception - Groups without an active Fluid Attacks service "
                         + "can not have Fluid Attacks staff"),
        new GraphQLError("Exception - Groups with any active Fluid Attacks service "
                         + "can only have Hackers provided by Fluid Attacks"),
      ]},
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_grant_stakeholder_access_mutate" },
      { action: "grant_group_level_role:analyst" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <ProjectStakeholdersView {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    let addUserModal: ReactWrapper = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Add stakeholder to this group"});
    expect(addUserModal)
      .toHaveLength(1);
    const emailInput: ReactWrapper = addUserModal
      .find({name: "email", type: "text"})
      .at(0)
      .find("input");
    emailInput.simulate("change", { target: { value: "unittest@test.com" } });
    const phoneNumberInput: ReactWrapper = addUserModal
      .find({name: "phoneNumber", type: "text"})
      .at(0)
      .find("input");
    phoneNumberInput.simulate("change", { target: { value: "+573123210123" } });
    const responsibilityInput: ReactWrapper = addUserModal
      .find({name: "responsibility", type: "text"})
      .at(0)
      .find("input");
    responsibilityInput.simulate("change", { target: { value: "Project Manager" } });
    const select: ReactWrapper = addUserModal.find("select")
      .findWhere((element: ReactWrapper) => element.contains("Analyst"))
      .at(0);
    select.simulate("change", { target: { value: "ANALYST" } });
    const form: ReactWrapper = addUserModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    addUserModal = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Add stakeholder to this group"});
    expect(addUserModal)
      .toHaveLength(0);
    expect(msgError)
      .toHaveBeenCalledTimes(8);
  });

  it("should handle error when remove stakeholder from the project", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: REMOVE_STAKEHOLDER_MUTATION,
        variables: {
          projectName: "TEST",
          userEmail: "user@gmail.com",
        },
      },
      result: { errors: [new GraphQLError("Access denied")] },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_remove_stakeholder_access_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <ProjectStakeholdersView {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const userInfo: ReactWrapper = wrapper.find("tr")
      .findWhere((element: ReactWrapper) => element.contains("user@gmail.com"))
      .at(0);
    userInfo.simulate("click");
    const removeButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Remove"))
      .at(0);
    removeButton.simulate("click");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgError)
      .toHaveBeenCalled();
  });

  it("should handle error when edit stakeholder from the project", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: EDIT_STAKEHOLDER_MUTATION,
        variables: {
          email: "user@gmail.com",
          phoneNumber: "+573123210123",
          projectName: "TEST",
          responsibility: "Project Manager",
          role: "ANALYST",
        },
      },
      result: { errors: [
        new GraphQLError("Access denied"),
        new GraphQLError("Exception - Invalid field in form"),
        new GraphQLError("Exception - Invalid characters"),
        new GraphQLError("Exception - Invalid phone number in form"),
        new GraphQLError("Exception - Groups without an active Fluid Attacks service "
                         + "can not have Fluid Attacks staff"),
        new GraphQLError("Exception - Groups with any active Fluid Attacks service "
                         + "can only have Hackers provided by Fluid Attacks"),
      ]},
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_edit_stakeholder_mutate" },
      { action: "grant_group_level_role:analyst" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <ProjectStakeholdersView {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const userInfo: ReactWrapper = wrapper.find("tr")
      .findWhere((element: ReactWrapper) => element.contains("user@gmail.com"))
      .at(0);
    userInfo.simulate("click");
    const editButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Edit"))
      .at(0);
    editButton.simulate("click");
    let editUserModal: ReactWrapper = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Edit stakeholder information"});
    expect(editUserModal)
      .toHaveLength(1);
    const phoneNumberInput: ReactWrapper = editUserModal
      .find({name: "phoneNumber", type: "text"})
      .at(0)
      .find("input");
    phoneNumberInput.simulate("change", { target: { value: "+573123210123" } });
    const responsibilityInput: ReactWrapper = editUserModal
      .find({name: "responsibility", type: "text"})
      .at(0)
      .find("input");
    responsibilityInput.simulate("change", { target: { value: "Project Manager" } });
    const select: ReactWrapper = editUserModal.find("select")
      .findWhere((element: ReactWrapper) => element.contains("Analyst"))
      .at(0);
    select.simulate("change", { target: { value: "ANALYST" } });
    const form: ReactWrapper = editUserModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    editUserModal = wrapper
      .find("Modal")
      .find({open: true, headerTitle: "Edit stakeholder information"});
    expect(editUserModal)
      .toHaveLength(0);
    expect(msgError)
      .toHaveBeenCalledTimes(6);
  });
});
