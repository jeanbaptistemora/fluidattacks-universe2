/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable react/jsx-props-no-spreading
  --------
  Best way to pass down props for test wrappers.
*/
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { GraphQLError } from "graphql";
import React from "react";

import { AddUserModal } from "scenes/Dashboard/components/AddUserModal";
import { GET_STAKEHOLDER } from "scenes/Dashboard/components/AddUserModal/queries";
import type { IAddStakeholderModalProps } from "scenes/Dashboard/components/AddUserModal/types";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

const functionMock: () => void = (): void => undefined;

describe("Add user modal", (): void => {
  const mockPropsAdd: IAddStakeholderModalProps = {
    action: "add",
    domainSuggestings: [],
    editTitle: "",
    groupName: "TEST",
    initialValues: {},
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    suggestions: [],
    title: "",
    type: "user",
  };

  const mockPropsEdit: IAddStakeholderModalProps = {
    action: "edit",
    domainSuggestings: [],
    editTitle: "edit title",
    groupName: "TEST",
    initialValues: {
      email: "user@test.com",
      role: "USER",
    },
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    suggestions: [],
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
    expect(typeof AddUserModal).toBe("function");
  });

  it("should handle errors when auto fill data", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider addTypename={true} mocks={mockError}>
        <AddUserModal {...mockPropsEdit} />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("userModal.emailPlaceholder")
      ).toHaveValue("user@test.com");
    });

    expect(screen.queryByText("edit title")).toBeInTheDocument();

    fireEvent.blur(screen.getByPlaceholderText("userModal.emailPlaceholder"));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    jest.clearAllMocks();
  });

  it("should render an add component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider addTypename={true} mocks={mocks}>
        <AddUserModal {...mockPropsAdd} />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("userModal.emailPlaceholder")
      ).toHaveValue("");
    });
  });

  it("should render an edit component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider addTypename={true} mocks={mocks}>
        <AddUserModal {...mockPropsEdit} />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("userModal.emailPlaceholder")
      ).toHaveValue("user@test.com");
    });
  });

  it("should auto fill data on inputs", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider addTypename={true} mocks={mocks}>
        <AddUserModal {...mockPropsAdd} />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("userModal.emailPlaceholder")
      ).toHaveValue("");
    });
    fireEvent.change(screen.getByRole("combobox", { name: "email" }), {
      target: { value: "unittest@test.com" },
    });
    fireEvent.blur(screen.getByRole("combobox", { name: "email" }));
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "responsibility" })
      ).toHaveValue("edited");
    });
  });

  it("should render user level role options", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "grant_user_level_role:admin" },
      { action: "grant_user_level_role:user" },
      { action: "grant_user_level_role:hacker" },
    ]);
    render(
      <MockedProvider addTypename={true} mocks={mocks}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <AddUserModal {...mockPropsAdd} groupName={undefined} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("combobox")).toHaveLength(2);
    });

    expect(screen.queryAllByRole("option")).toHaveLength(4);
    expect(
      screen.getByRole("option", {
        name: "userModal.roles.admin",
        selected: false,
      })
    ).toHaveValue("ADMIN");
    expect(
      screen.getByRole("option", {
        name: "userModal.roles.hacker",
        selected: false,
      })
    ).toHaveValue("HACKER");
    expect(
      screen.getByRole("option", {
        name: "userModal.roles.user",
        selected: false,
      })
    ).toHaveValue("USER");
    expect(
      screen.getByRole("option", { name: "", selected: true })
    ).toHaveValue("");
  });
});
