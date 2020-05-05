import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { shallow, ShallowWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { Provider } from "react-redux";
import { Action, createStore, Store } from "redux";
import wait from "waait";
import { addUserModal as AddUserModal } from "./index";
import { GET_USER } from "./queries";
import { IAddUserModalProps } from "./types";

const functionMock: (() => void) = (): void => undefined;

describe("Add user modal", () => {

  const mockPropsAdd: IAddUserModalProps = {
    initialValues: {},
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    projectName: "TEST",
    type: "add",
  };

  const mockPropsEdit: IAddUserModalProps = {
    initialValues: {},
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    projectName: "TEST",
    type: "edit",
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
