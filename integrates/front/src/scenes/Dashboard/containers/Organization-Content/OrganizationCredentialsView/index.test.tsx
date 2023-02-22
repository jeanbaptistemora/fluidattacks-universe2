import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
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
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
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

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_credentials_mutate" },
    ]);
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
                  azureOrganization: "testorg1",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  isPat: true,
                  isToken: true,
                  name: "Credentials test",
                  oauthType: "",
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
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <OrganizationCredentials
            organizationId={"ORG#15eebe68-e9ce-4611-96f5-13d6562687e1"}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("Credentials test")).toBeInTheDocument();
    });

    expect(screen.getByText("owner@test.com")).toBeInTheDocument();

    expect(
      screen.queryByText("profile.credentialsModal.title")
    ).not.toBeInTheDocument();

    await userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.actionButtons.addButton.text",
      })
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("profile.credentialsModal.title")
      ).toBeInTheDocument();
    });

    expect(
      screen.getByRole("combobox", { name: "typeCredential" })
    ).toHaveValue("SSH");
    expect(screen.queryByRole("textbox", { name: "key" })).toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "password" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "azureOrganization" })
    ).not.toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "typeCredential" }),
      ["TOKEN"]
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "azureOrganization" })
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByRole("textbox", { name: "key" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "password" })
    ).not.toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "typeCredential" }),
      ["USER"]
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "password" })
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByRole("textbox", { name: "key" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "azureOrganization" })
    ).not.toBeInTheDocument();
  });

  it("should render errors", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_CREDENTIALS,
          variables: {
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: { errors: [new GraphQLError("Access denied")] },
      },
    ];
    const mockedMutations: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_CREDENTIALS,
          variables: {
            credentials: {
              azureOrganization: "testorg1",
              isPat: true,
              name: "New name",
              token: "New token",
              type: "HTTPS",
            },
            organizationId: "ORG#15eebe68-e9ce-4611-96f5-13d6562687e1",
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - A credential exists with the same name"
            ),
            new GraphQLError(
              "Exception - Field cannot fill with blank characters"
            ),
            new GraphQLError("Exception - Password should start with a letter"),
            new GraphQLError(
              "Exception - Password should include at least one number"
            ),
            new GraphQLError(
              "Exception - Password should include lowercase characters"
            ),
            new GraphQLError(
              "Exception - Password should include uppercase characters"
            ),
            new GraphQLError(
              "Exception - Password should include symbols characters"
            ),
            new GraphQLError(
              "Exception - Password should not include sequentials characters"
            ),
          ],
        },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_credentials_mutate" },
    ]);
    const mockedAuth = {
      tours: {
        newGroup: false,
        newRiskExposure: true,
        newRoot: false,
        welcome: true,
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
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.actionButtons.addButton.text",
      })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "New name"
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "typeCredential" }),
      [
        screen.getByText(
          "organization.tabs.credentials.credentialsModal.form.auth.azureToken"
        ),
      ]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "token" }),
      "New token"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "azureOrganization" }),
      "testorg1"
    );
    await userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.credentialsModal.form.add",
      })
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(8);
    });

    jest.clearAllMocks();
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
                  azureOrganization: null,
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  isPat: false,
                  isToken: false,
                  name: "Credentials test",
                  oauthType: "",
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
              azureOrganization: "testorg1",
              isPat: true,
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
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_credentials_mutate" },
    ]);
    const mockedAuth = {
      tours: {
        newGroup: false,
        newRiskExposure: true,
        newRoot: false,
        welcome: true,
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
    await userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.actionButtons.addButton.text",
      })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "New name"
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "typeCredential" }),
      [
        screen.getByText(
          "organization.tabs.credentials.credentialsModal.form.auth.azureToken"
        ),
      ]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "token" }),
      "New token"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "azureOrganization" }),
      "testorg1"
    );
    await userEvent.click(
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
                  azureOrganization: null,
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  isPat: false,
                  isToken: false,
                  name: "Credentials test",
                  oauthType: "",
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
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_remove_credentials_mutate" },
    ]);
    const mockedAuth = {
      tours: {
        newGroup: false,
        newRiskExposure: true,
        newRoot: false,
        welcome: true,
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
    await userEvent.click(screen.getByRole("radio"));
    await userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.actionButtons.removeButton.text",
      })
    );
    await userEvent.click(
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
                  azureOrganization: null,
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  isPat: false,
                  isToken: false,
                  name: "Credentials test",
                  oauthType: "",
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
              password:
                "lorem.ipsum,Dolor.sit:am3t;consectetur@adipiscing$elit",
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
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_credentials_mutate" },
    ]);
    const mockedAuth = {
      tours: {
        newGroup: false,
        newRiskExposure: true,
        newRoot: false,
        welcome: true,
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
    await userEvent.click(screen.getByRole("radio"));
    await userEvent.click(
      screen.getByRole("button", {
        name: "organization.tabs.credentials.actionButtons.editButton.text",
      })
    );
    await userEvent.click(screen.getByRole("checkbox", { name: "newSecrets" }));
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "typeCredential" }),
      ["USER"]
    );
    await userEvent.clear(screen.getByRole("textbox", { name: "user" }));
    await userEvent.type(
      screen.getByRole("textbox", { name: "user" }),
      "User test"
    );

    await userEvent.clear(screen.getByRole("textbox", { name: "password" }));
    await userEvent.type(
      screen.getByRole("textbox", { name: "password" }),
      "lorem.ipsum,Dolor.sit:am3t;consectetur@adipiscing$elit"
    );
    await userEvent.click(
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
