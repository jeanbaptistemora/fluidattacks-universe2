import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../../store";
import { msgError } from "../../../../../utils/notifications";
import { addUserModal as AddUserModal } from "./index";
import { GET_USER } from "./queries";
import { IAddUserModalProps } from "./types";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});
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

    },
    {
      request: {
        query: GET_USER,
        variables: {
          projectName: "TEST",
          userEmail: "unittest@test.com",
        },
      },
      result: {
        data: {
          user: {
            __typename: "User",
            organization: "unittesting",
            phoneNumber: "+573123210123",
            responsibility: "edited",
          },
        },
      },
    },
  ];

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
    },
    {
      request: {
        query: GET_USER,
        variables: {
          projectName: "TEST",
          userEmail: "unittest@test.com",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

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

  it("should auto fill data on inputs", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <AddUserModal {...mockPropsAdd} />
        </MockedProvider>
      </Provider>,
    );
    const emailInput: ReactWrapper = wrapper
      .find({name: "email", type: "text"})
      .at(0)
      .find("input");
    emailInput.simulate("change", { target: { value: "unittest@test.com", name: "email" } });
    emailInput.simulate("blur");
    await act(async () => { await wait(0); wrapper.update(); });

    const organizationInput: ReactWrapper = wrapper
      .find({name: "organization", type: "text"})
      .at(0)
      .find("input");
    const phoneNumberInput: ReactWrapper = wrapper
      .find({name: "phoneNumber", type: "text"})
      .at(0)
      .find("input");
    const responsibilityInput: ReactWrapper = wrapper
      .find({name: "responsibility", type: "text"})
      .at(0)
      .find("input");
    expect(organizationInput.prop("value"))
      .toEqual("unittesting");
    expect(phoneNumberInput.prop("value"))
      .toEqual("+573123210123");
    expect(responsibilityInput.prop("value"))
      .toEqual("edited");
  });

  it("should handle errors when auto fill data", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={true}>
          <AddUserModal {...mockPropsAdd} />
        </MockedProvider>
      </Provider>,
    );
    const emailInput: ReactWrapper = wrapper
      .find({name: "email", type: "text"})
      .at(0)
      .find("input");
    emailInput.simulate("change", { target: { value: "unittest@test.com", name: "email" } });
    emailInput.simulate("blur");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgError)
      .toHaveBeenCalled();
  });
});
