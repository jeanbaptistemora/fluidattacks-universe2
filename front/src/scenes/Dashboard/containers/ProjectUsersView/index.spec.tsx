import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../store/index";
import { authzContext } from "../../../../utils/authz/config";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import { ProjectUsersView } from "./index";
import { ADD_USER_MUTATION, EDIT_USER_MUTATION, GET_USERS, REMOVE_USER_MUTATION } from "./queries";
import { IProjectUsersViewProps } from "./types";

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

  const mockProps: IProjectUsersViewProps = {
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
        query: GET_USERS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            users: [{
              email: "user@gmail.com",
              firstLogin: "2017-09-05 15:00:00",
              lastLogin: "[3, 81411]",
              organization: "TEST",
              phoneNumber: "-",
              responsibility: "-",
              role: "customer",
            }],
          },
        },
      },
    },
    {
      request: {
        query: GET_USERS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            users: [
              {
                email: "user@gmail.com",
                firstLogin: "2017-09-05 15:00:00",
                lastLogin: "[3, 81411]",
                organization: "TEST",
                phoneNumber: "-",
                responsibility: "-",
                role: "customer",
              },
              {
                email: "unittest@test.com",
                firstLogin: "2017-09-05 15:00:00",
                lastLogin: "[3, 81411]",
                organization: "TEST",
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
        query: GET_USERS,
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
    expect(typeof (ProjectUsersView))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={false}>
          <ProjectUsersView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an add user component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectUsersView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an edit user component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <ProjectUsersView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should open a modal to add user", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_user__do_grant_user_access" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <ProjectUsersView {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    let addUserModal: ReactWrapper = wrapper
      .find("modal")
      .find({open: true, headerTitle: "Add user to this project"});
    expect(addUserModal)
      .toHaveLength(0);
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    await act(async () => { await wait(0); wrapper.update(); });
    addUserModal = wrapper
      .find("modal")
      .find({open: true, headerTitle: "Add user to this project"});
    expect(addUserModal)
      .toHaveLength(1);
  });

  it("should open a modal to edit user", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_user__do_edit_user" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <ProjectUsersView {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    let editUserModal: ReactWrapper = wrapper
      .find("modal")
      .find({open: true, headerTitle: "Edit user information"});
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
      .find("modal")
      .find({open: true, headerTitle: "Edit user information"});
    expect(editUserModal)
      .toHaveLength(1);
  });

  it("should add user to the project", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: ADD_USER_MUTATION,
        variables: {
          email: "unittest@test.com",
          organization: "unittesting",
          phoneNumber: "+573123210123",
          projectName: "TEST",
          responsibility: "Project Manager",
          role: "ANALYST",
        },
      },
      result: { data: { grantUserAccess : { success: true, grantedUser: {email: "unittest@test.com"} } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_user__do_grant_user_access" },
      { action: "grant_group_level_role:analyst" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <ProjectUsersView {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    let addUserModal: ReactWrapper = wrapper
      .find("modal")
      .find({open: true, headerTitle: "Add user to this project"});
    expect(addUserModal)
      .toHaveLength(1);
    const emailInput: ReactWrapper = addUserModal
      .find({name: "email", type: "text"})
      .at(0)
      .find("input");
    emailInput.simulate("change", { target: { value: "unittest@test.com" } });
    const organizationInput: ReactWrapper = addUserModal
      .find({name: "organization", type: "text"})
      .at(0)
      .find("input");
    organizationInput.simulate("change", { target: { value: "unittesting" } });
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
      .find("modal")
      .find({open: true, headerTitle: "Add user to this project"});
    expect(addUserModal)
      .toHaveLength(0);
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should remove user from the project", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: REMOVE_USER_MUTATION,
        variables: {
          projectName: "TEST",
          userEmail: "user@gmail.com",
        },
      },
      result: { data: { removeUserAccess : { success: true, removedEmail: "user@gmail.com" } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_user__do_remove_user_access" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <ProjectUsersView {...mockProps} />
          </authzContext.Provider>
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

  it("should edit user from the project", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: EDIT_USER_MUTATION,
        variables: {
          email: "user@gmail.com",
          firstLogin: "2017-09-05",
          lastLogin: "3 days ago",
          organization: "unittesting",
          phoneNumber: "+573123210123",
          projectName: "TEST",
          responsibility: "Project Manager",
          role: "ANALYST",
          uniqueId: 0,
        },
      },
      result: { data: { editUser : { success: true } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_user__do_edit_user" },
      { action: "grant_group_level_role:analyst" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <ProjectUsersView {...mockProps} />
          </authzContext.Provider>
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
      .find("modal")
      .find({open: true, headerTitle: "Edit user information"});
    expect(editUserModal)
      .toHaveLength(1);
    const organizationInput: ReactWrapper = editUserModal
      .find({name: "organization", type: "text"})
      .at(0)
      .find("input");
    organizationInput.simulate("change", { target: { value: "unittesting" } });
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
      .find("modal")
      .find({open: true, headerTitle: "Edit user information"});
    expect(editUserModal)
      .toHaveLength(0);
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should handle errors when add user to the project", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: ADD_USER_MUTATION,
        variables: {
          email: "unittest@test.com",
          organization: "unittesting",
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
        new GraphQLError("Exception - Invalid phone number in form"),
        new GraphQLError("Exception - Invalid email address in form"),
      ]},
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_user__do_grant_user_access" },
      { action: "grant_group_level_role:analyst" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <ProjectUsersView {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    let addUserModal: ReactWrapper = wrapper
      .find("modal")
      .find({open: true, headerTitle: "Add user to this project"});
    expect(addUserModal)
      .toHaveLength(1);
    const emailInput: ReactWrapper = addUserModal
      .find({name: "email", type: "text"})
      .at(0)
      .find("input");
    emailInput.simulate("change", { target: { value: "unittest@test.com" } });
    const organizationInput: ReactWrapper = addUserModal
      .find({name: "organization", type: "text"})
      .at(0)
      .find("input");
    organizationInput.simulate("change", { target: { value: "unittesting" } });
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
      .find("modal")
      .find({open: true, headerTitle: "Add user to this project"});
    expect(addUserModal)
      .toHaveLength(0);
    expect(msgError)
      .toHaveBeenCalledTimes(5);
  });
});
