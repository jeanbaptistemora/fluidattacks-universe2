/* eslint-disable @typescript-eslint/no-unsafe-return */
/* eslint-disable react/jsx-props-no-spreading
  --------
  Best way to pass down props and allow lazy updates for test wrappers.
*/
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import wait from "waait";

import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import { GET_STAKEHOLDER } from "scenes/Dashboard/components/AddUserModal/queries";
import type { IAddStakeholderModalProps } from "scenes/Dashboard/components/AddUserModal/types";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

const functionMock: () => void = (): void => undefined;

describe("Add user modal", (): void => {
  const mockPropsAdd: IAddStakeholderModalProps = {
    action: "add",
    editTitle: "",
    groupName: "TEST",
    initialValues: {},
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    title: "",
    type: "user",
  };

  const mockPropsEdit: IAddStakeholderModalProps = {
    action: "edit",
    editTitle: "",
    groupName: "TEST",
    initialValues: {},
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    title: "",
    type: "user",
  };

  const mocks: MockedResponse[] = [
    {
      request: {
        query: GET_STAKEHOLDER,
        variables: {
          entity: "GROUP",
          groupName: "TEST",
          organizationId: "-",
          userEmail: "user@test.com",
        },
      },
      result: {
        data: {
          stakeholder: {
            __typename: "User",
            email: "user@test.com",
            responsibility: "tester",
          },
        },
      },
    },
    {
      request: {
        query: GET_STAKEHOLDER,
        variables: {
          entity: "GROUP",
          groupName: "TEST",
          organizationId: "-",
          userEmail: "unittest@test.com",
        },
      },
      result: {
        data: {
          stakeholder: {
            __typename: "User",
            email: "unittest@test.com",
            responsibility: "edited",
          },
        },
      },
    },
  ];

  const mockError: MockedResponse[] = [
    {
      request: {
        query: GET_STAKEHOLDER,
        variables: {
          entity: "GROUP",
          groupName: "TEST",
          organizationId: "-",
          userEmail: "user@test.com",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
    {
      request: {
        query: GET_STAKEHOLDER,
        variables: {
          entity: "GROUP",
          groupName: "TEST",
          organizationId: "-",
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
      <MockedProvider addTypename={true} mocks={mockError}>
        <AddUserModal {...mockPropsAdd} />
      </MockedProvider>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should render an add component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <MockedProvider addTypename={true} mocks={mocks}>
        <AddUserModal {...mockPropsAdd} />
      </MockedProvider>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should render an edit component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <MockedProvider addTypename={true} mocks={mocks}>
        <AddUserModal {...mockPropsEdit} />
      </MockedProvider>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should auto fill data on inputs", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={true} mocks={mocks}>
        <AddUserModal {...mockPropsAdd} />
      </MockedProvider>
    );
    const emailInput = (): ReactWrapper =>
      wrapper.find({ name: "email", type: "text" }).at(0).find("input");
    const responsibilityInput = (): ReactWrapper =>
      wrapper
        .find({ name: "responsibility", type: "text" })
        .at(0)
        .find("input");

    await act(async (): Promise<void> => {
      emailInput().simulate("change", {
        target: { name: "email", value: "unittest@test.com" },
      });
      emailInput().simulate("blur", {
        target: { name: "email", value: "unittest@test.com" },
      });
      const delay = 200;
      await wait(delay);

      wrapper.update();
    });

    expect(responsibilityInput().prop("value")).toStrictEqual("edited");
  });

  it("should handle errors when auto fill data", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={true} mocks={mockError}>
        <AddUserModal {...mockPropsAdd} />
      </MockedProvider>
    );
    const emailInput: ReactWrapper = wrapper
      .find({ name: "email", type: "text" })
      .at(0)
      .find("input");
    await act(async (): Promise<void> => {
      emailInput.simulate("change", {
        target: { name: "email", value: "unittest@test.com" },
      });
      emailInput.simulate("blur", {
        target: { name: "email", value: "unittest@test.com" },
      });
      await wait(0);

      wrapper.update();
    });

    expect(msgError).toHaveBeenCalledWith("There is an error :(");
  });

  it("should render user level role options", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "grant_user_level_role:admin" },
      { action: "grant_user_level_role:customer" },
      { action: "grant_user_level_role:hacker" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={true} mocks={mocks}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <AddUserModal {...mockPropsAdd} groupName={undefined} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const options: ReactWrapper = wrapper.find("option");
    const adminOption: ReactWrapper = options.find({ value: "ADMIN" });

    expect(adminOption).toHaveLength(1);

    const userOption: ReactWrapper = options.find({ value: "CUSTOMER" });

    expect(userOption).toHaveLength(1);

    const hackerOption: ReactWrapper = options.find({
      value: "HACKER",
    });

    expect(hackerOption).toHaveLength(1);
  });
});
