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
import { ProjectUsersView } from "./index";
import { GET_USERS } from "./queries";
import { IProjectUsersViewProps } from "./types";

describe("Project users view", () => {

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
    }];

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
});
