/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable react/jsx-no-constructed-context-values */
import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import {
  ADD_CREDENTIALS,
  GET_ORGANIZATION_CREDENTIALS,
  REMOVE_CREDENTIALS,
  UPDATE_CREDENTIALS,
} from "./queries";

import { OrganizationCredentials } from ".";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("organization credentials view", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationCredentials).toBe("function");
  });

  it("should list organization's credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_CREDENTIALS,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  owner: "owner@test.com",
                  type: "HTTPS",
                },
              ],
              name: "org-test",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockedQueries}>
        <authzPermissionsContext.Provider value={new PureAbility([])}>
          <OrganizationCredentials
            organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("Credentials test")).toBeInTheDocument();
      expect(screen.getByText("HTTPS")).toBeInTheDocument();
      expect(screen.getByText("owner@test.com")).toBeInTheDocument();
    });
  });

  it("should add credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_CREDENTIALS,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  owner: "owner@test.com",
                  type: "HTTPS",
                },
              ],
              name: "org-test",
            },
          },
        },
      },
    ];
    const mockedMutations: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_CREDENTIALS,
          variables: {
            credentials: {
              name: "New name",
              token: "New token",
              type: "HTTPS",
            },
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: { data: { addCredentials: { success: true } } },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_credentials_mutate" },
    ]);
    const mockedAuth = {
      tours: {
        newGroup: false,
        newRoot: false,
      },
      userEmail: "owner@test.com",
      userName: "owner",
    };
    render(
      <MockedProvider
        addTypename={false}
        mocks={[...mockedQueries, ...mockedMutations]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <authContext.Provider value={mockedAuth}>
            <OrganizationCredentials
              organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
            />
          </authContext.Provider>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("owner@test.com")).toBeInTheDocument();
    });
    userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.actionButtons.addButton.text",
      })
    );
    userEvent.type(screen.getByRole("textbox", { name: "name" }), "New name");
    userEvent.selectOptions(screen.getByRole("combobox", { name: "type" }), [
      screen.getByText(
        "organization.tabs.credentials.credentialsModal.form.type.https"
      ),
    ]);
    userEvent.type(screen.getByRole("textbox", { name: "token" }), "New token");
    userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.credentialsModal.form.add",
      })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "organization.tabs.credentials.alerts.addSuccess",
        "groupAlerts.titleSuccess"
      );
    });
  });

  it("should remove credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_CREDENTIALS,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  owner: "owner@test.com",
                  type: "HTTPS",
                },
              ],
              name: "org-test",
            },
          },
        },
      },
    ];
    const mockedMutations: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_CREDENTIALS,
          variables: {
            credentialsId: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: { data: { removeCredentials: { success: true } } },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_credentials_mutate" },
    ]);
    const mockedAuth = {
      tours: {
        newGroup: false,
        newRoot: false,
      },
      userEmail: "owner@test.com",
      userName: "owner",
    };
    render(
      <MockedProvider
        addTypename={false}
        mocks={[...mockedQueries, ...mockedMutations]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <authContext.Provider value={mockedAuth}>
            <OrganizationCredentials
              organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
            />
          </authContext.Provider>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("owner@test.com")).toBeInTheDocument();
    });
    userEvent.click(screen.getByRole("radio"));
    userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.actionButtons.removeButton.text",
      })
    );
    userEvent.click(
      screen.getByRole("button", {
        name: "components.modal.confirm",
      })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "organization.tabs.credentials.alerts.removeSuccess",
        "groupAlerts.titleSuccess"
      );
    });
  });

  it("should edit credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_CREDENTIALS,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  owner: "owner@test.com",
                  type: "HTTPS",
                },
              ],
              name: "org-test",
            },
          },
        },
      },
    ];
    const mockedMutations: readonly MockedResponse[] = [
      {
        request: {
          query: UPDATE_CREDENTIALS,
          variables: {
            credentials: {
              name: "Credentials test",
              password: "Password test",
              type: "HTTPS",
              user: "User test",
            },
            credentialsId: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: { data: { updateCredentials: { success: true } } },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_credentials_mutate" },
    ]);
    const mockedAuth = {
      tours: {
        newGroup: false,
        newRoot: false,
      },
      userEmail: "owner@test.com",
      userName: "owner",
    };
    render(
      <MockedProvider
        addTypename={false}
        mocks={[...mockedQueries, ...mockedMutations]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <authContext.Provider value={mockedAuth}>
            <OrganizationCredentials
              organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
            />
          </authContext.Provider>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("owner@test.com")).toBeInTheDocument();
    });
    userEvent.click(screen.getByRole("radio"));
    userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.actionButtons.editButton.text",
      })
    );
    userEvent.click(screen.getByRole("checkbox", { name: "newSecrets" }));
    userEvent.selectOptions(screen.getByRole("combobox", { name: "type" }), [
      screen.getByText(
        "organization.tabs.credentials.credentialsModal.form.type.https"
      ),
    ]);
    userEvent.selectOptions(screen.getByRole("combobox", { name: "auth" }), [
      screen.getByText(
        "organization.tabs.credentials.credentialsModal.form.auth.user"
      ),
    ]);
    userEvent.type(screen.getByRole("textbox", { name: "user" }), "User test");
    userEvent.type(
      screen.getByRole("textbox", { name: "password" }),
      "Password test"
    );
    userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.credentialsModal.form.edit",
      })
    );
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "organization.tabs.credentials.alerts.editSuccess",
        "groupAlerts.titleSuccess"
      );
    });
  });
});
