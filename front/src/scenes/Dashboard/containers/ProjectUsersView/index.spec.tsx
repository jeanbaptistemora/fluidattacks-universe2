import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../store/index";
import ProjectUsersView from "./index";
import { GET_USERS } from "./queries";
import { IProjectUsersViewProps } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Project users view", () => {

  const mockPropsAdd: IProjectUsersViewProps = {
    addModal: {
      initialValues: {},
      open: false,
      type: "add",
    },
    match: {
      isExact: true,
      params: {projectName: "TEST"},
      path: "/",
      url: "",
    },
    onCloseUsersModal: functionMock,
    onOpenModal: functionMock,
    userRole: "manager",
  };

  const mockPropsEdit: IProjectUsersViewProps = {
    addModal: {
      initialValues: {},
      open: true,
      type: "edit",
    },
    match: {
      isExact: true,
      params: {projectName: "TEST"},
      path: "/",
      url: "",
    },
    onCloseUsersModal: functionMock,
    onOpenModal: functionMock,
    userRole: "manager",
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
            __typename: "Project",
            users: [{
              __typename: "User",
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

  it("should return a object", () => {
    expect(typeof (ProjectUsersView))
      .toEqual("object");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={true}>
          <ProjectUsersView {...mockPropsAdd} />
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
        <MockedProvider mocks={mocks} addTypename={true}>
          <ProjectUsersView {...mockPropsAdd} />
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
        <MockedProvider mocks={mocks} addTypename={true}>
          <ProjectUsersView {...mockPropsEdit} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
