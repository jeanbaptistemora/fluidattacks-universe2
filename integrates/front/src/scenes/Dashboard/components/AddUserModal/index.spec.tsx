/* eslint-disable react/jsx-props-no-spreading
  --------
  Best way to pass down props.
*/
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import { GET_USER } from "scenes/Dashboard/components/AddUserModal/queries";
import type { IAddStakeholderModalProps } from "scenes/Dashboard/components/AddUserModal/types";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";

jest.mock(
  "../../../../utils/notifications",
  (): Dictionary => {
    const mockedNotifications: Dictionary<
      () => Dictionary
    > = jest.requireActual("../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

const functionMock: () => void = (): void => undefined;

describe("Add user modal", (): void => {
  const mockPropsAdd: IAddStakeholderModalProps = {
    action: "add",
    editTitle: "",
    initialValues: {},
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    projectName: "TEST",
    title: "",
    type: "user",
  };

  const mockPropsEdit: IAddStakeholderModalProps = {
    action: "edit",
    editTitle: "",
    initialValues: {},
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    projectName: "TEST",
    title: "",
    type: "user",
  };

  const mocks: MockedResponse[] = [
    {
      request: {
        query: GET_USER,
        variables: {
          entity: "PROJECT",
          organizationId: "-",
          projectName: "TEST",
          userEmail: "user@test.com",
        },
      },
      result: {
        data: {
          stakeholder: {
            __typename: "User",
            email: "user@test.com",
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
          entity: "PROJECT",
          organizationId: "-",
          projectName: "TEST",
          userEmail: "unittest@test.com",
        },
      },
      result: {
        data: {
          stakeholder: {
            __typename: "User",
            email: "unittest@test.com",
            phoneNumber: "+573123210123",
            responsibility: "edited",
          },
        },
      },
    },
  ];

  const mockError: MockedResponse[] = [
    {
      request: {
        query: GET_USER,
        variables: {
          entity: "PROJECT",
          organizationId: "-",
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
          entity: "PROJECT",
          organizationId: "-",
          projectName: "TEST",
          userEmail: "unittest@test.com",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddUserModal).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <MockedProvider addTypename={true} mocks={mockError}>
          <AddUserModal {...mockPropsAdd} />
        </MockedProvider>
      </Provider>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should render an add component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <AddUserModal {...mockPropsAdd} />
        </MockedProvider>
      </Provider>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should render an edit component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <AddUserModal {...mockPropsEdit} />
        </MockedProvider>
      </Provider>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should auto fill data on inputs", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <AddUserModal {...mockPropsAdd} />
        </MockedProvider>
      </Provider>
    );
    const emailInput: ReactWrapper = wrapper
      .find({ name: "email", type: "text" })
      .at(0)
      .find("input");
    emailInput.simulate("change", {
      target: { name: "email", value: "unittest@test.com" },
    });
    emailInput.simulate("blur");

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          const phoneNumberInput: ReactWrapper = wrapper
            .find({ name: "phoneNumber", type: "text" })
            .at(0)
            .find("input");
          const responsibilityInput: ReactWrapper = wrapper
            .find({ name: "responsibility", type: "text" })
            .at(0)
            .find("input");

          expect(phoneNumberInput.prop("value")).toStrictEqual(
            "+57 (312) 321 0123"
          );
          expect(responsibilityInput.prop("value")).toStrictEqual("edited");
        });
      }
    );
  });

  it("should handle errors when auto fill data", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={true} mocks={mockError}>
          <AddUserModal {...mockPropsAdd} />
        </MockedProvider>
      </Provider>
    );
    const emailInput: ReactWrapper = wrapper
      .find({ name: "email", type: "text" })
      .at(0)
      .find("input");
    emailInput.simulate("change", {
      target: { name: "email", value: "unittest@test.com" },
    });
    emailInput.simulate("blur");
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(msgError).toHaveBeenCalledWith("There is an error :(");
  });

  it("should render user level role options", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "grant_user_level_role:admin" },
      { action: "grant_user_level_role:customer" },
      { action: "grant_user_level_role:analyst" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <AddUserModal {...mockPropsAdd} projectName={undefined} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const options: ReactWrapper = wrapper.find("option");
    const adminOption: ReactWrapper = options.find({ value: "ADMIN" });

    expect(adminOption).toHaveLength(1);

    const userOption: ReactWrapper = options.find({ value: "CUSTOMER" });

    expect(userOption).toHaveLength(1);

    const analystOption: ReactWrapper = options.find({
      value: "ANALYST",
    });

    expect(analystOption).toHaveLength(1);
  });
});
