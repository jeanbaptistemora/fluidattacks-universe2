import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import React from "react";
import { Provider } from "react-redux";
import { Action, createStore, Store } from "redux";
import wait from "waait";
import { addUserModal as AddUserModal } from "./index";
import { GET_USER } from "./queries";
import { IAddUserModalProps } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Add user modal", () => {

  const mockPropsAdd: IAddUserModalProps = {
    initialValues: {},
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    projectName: "TEST",
    type: "add",
    userRole: "admin",
  };

  const mockPropsEdit: IAddUserModalProps = {
    initialValues: {},
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    projectName: "TEST",
    type: "edit",
    userRole: "admin",
  };

  const store: Store<{}, Action<{}>> = createStore(() => ({}));

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_USER,
        variables: {
          projectName: "TEST",
          userEmail: "user@test.com",
        },
      },
      result: {
        data: {
          user: {
            __typename: "User",
            organization: "Test",
            phoneNumber: "+573123456791",
            responsibility: "tester",
          },
        },
      },
  }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_USER,
        variables: {
          projectName: "TEST",
          userEmail: "user@test.com",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
  }];

  it("should return a function", () => {
    expect(typeof (AddUserModal))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={true}>
          <AddUserModal {...mockPropsAdd} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an add component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <AddUserModal {...mockPropsAdd} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an edit component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <AddUserModal {...mockPropsEdit} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
