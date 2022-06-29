import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import {
  ADD_CREDENTIALS,
  GET_STAKEHOLDER_CREDENTIALS,
  GET_STAKEHOLDER_ORGANIZATIONS,
  REMOVE_CREDENTIALS,
  UPDATE_CREDENTIALS,
} from "./queries";

import { CredentialsModal } from ".";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("credentials modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof CredentialsModal).toBe("function");
  });

  it("should list stakeholder's credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();

    const mockQuery: MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDER_CREDENTIALS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  organization: {
                    __typename: "Organization",
                    id: "c966d57a-adde-43c3-bd47-1770002aa122",
                    name: "Organization name",
                  },
                  type: "HTTPS",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_STAKEHOLDER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  id: "c966d57a-adde-43c3-bd47-1770002aa122",
                  name: "Organization name",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockQuery}>
        <authzPermissionsContext.Provider value={new PureAbility([])}>
          <CredentialsModal onClose={handleOnClose} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("Credentials test")).toBeInTheDocument();
      expect(screen.getByText("Organization name")).toBeInTheDocument();
    });
  });

  it("should add credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();

    const mockQuery: MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDER_CREDENTIALS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  organization: {
                    __typename: "Organization",
                    id: "c966d57a-adde-43c3-bd47-1770002aa122",
                    name: "Organization name",
                  },
                  type: "HTTPS",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_STAKEHOLDER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  id: "c966d57a-adde-43c3-bd47-1770002aa122",
                  name: "Organization name",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_CREDENTIALS,
          variables: {
            credentials: {
              name: "New name",
              token: "New token",
              type: "HTTPS",
            },
            organizationId: "c966d57a-adde-43c3-bd47-1770002aa122",
          },
        },
        result: { data: { addCredentials: { success: true } } },
      },
    ];

    render(
      <MockedProvider
        addTypename={false}
        mocks={mockQuery.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={new PureAbility([])}>
          <CredentialsModal onClose={handleOnClose} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("Credentials test")).toBeInTheDocument();
      expect(screen.getByText("Organization name")).toBeInTheDocument();
    });

    userEvent.click(
      screen.getByRole("button", {
        name: "profile.credentialsModal.actionButtons.addButton.text",
      })
    );
    userEvent.type(screen.getByRole("textbox", { name: "name" }), "New name");
    userEvent.click(screen.getByRole("combobox", { name: "organization" }));

    userEvent.selectOptions(
      screen.getByRole("combobox", { name: "organization" }),
      [screen.getByText("Organization name")]
    );
    userEvent.click(screen.getByText("profile.credentialsModal.form.https"));
    userEvent.click(
      screen.getByText("profile.credentialsModal.form.httpsType.accessToken")
    );
    userEvent.type(
      screen.getByRole("textbox", { name: "accessToken" }),
      "New token"
    );
    userEvent.click(
      screen.getByRole("button", {
        name: "profile.credentialsModal.form.add",
      })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "profile.credentialsModal.alerts.addSuccess",
        "groupAlerts.titleSuccess"
      );
    });

    expect(handleOnClose).toHaveBeenCalledTimes(0);

    jest.clearAllMocks();
  });

  it("should remove credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();

    const mockQuery: MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDER_CREDENTIALS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  organization: {
                    __typename: "Organization",
                    id: "c966d57a-adde-43c3-bd47-1770002aa122",
                    name: "Organization name",
                  },
                  type: "HTTPS",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_STAKEHOLDER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  id: "c966d57a-adde-43c3-bd47-1770002aa122",
                  name: "Organization name",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_CREDENTIALS,
          variables: {
            credentialsId: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
            organizationId: "c966d57a-adde-43c3-bd47-1770002aa122",
          },
        },
        result: { data: { removeCredentials: { success: true } } },
      },
    ];

    render(
      <MockedProvider
        addTypename={false}
        mocks={mockQuery.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={new PureAbility([])}>
          <CredentialsModal onClose={handleOnClose} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("Credentials test")).toBeInTheDocument();
      expect(screen.getByText("Organization name")).toBeInTheDocument();
    });

    userEvent.click(screen.getByRole("button", { name: "trash-button" }));
    userEvent.click(
      screen.getByRole("button", { name: "components.modal.confirm" })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "profile.credentialsModal.alerts.removeSuccess",
        "groupAlerts.titleSuccess"
      );
    });

    expect(handleOnClose).toHaveBeenCalledTimes(0);

    jest.clearAllMocks();
  });

  it("should update credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();

    const mockQuery: MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDER_CREDENTIALS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  organization: {
                    __typename: "Organization",
                    id: "c966d57a-adde-43c3-bd47-1770002aa122",
                    name: "Organization name",
                  },
                  type: "HTTPS",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_STAKEHOLDER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  id: "c966d57a-adde-43c3-bd47-1770002aa122",
                  name: "Organization name",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    const mocksMutation: readonly MockedResponse[] = [
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
            organizationId: "c966d57a-adde-43c3-bd47-1770002aa122",
          },
        },
        result: { data: { updateCredentials: { success: true } } },
      },
    ];

    render(
      <MockedProvider
        addTypename={false}
        mocks={mockQuery.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={new PureAbility([])}>
          <CredentialsModal onClose={handleOnClose} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("Credentials test")).toBeInTheDocument();
      expect(screen.getByText("Organization name")).toBeInTheDocument();
    });

    userEvent.click(screen.getByRole("button", { name: "pen-button" }));
    userEvent.click(screen.getByRole("checkbox", { name: "newSecrets" }));
    userEvent.click(screen.getByText("profile.credentialsModal.form.https"));
    userEvent.type(screen.getByRole("textbox", { name: "user" }), "User test");
    userEvent.type(
      screen.getByRole("textbox", { name: "password" }),
      "Password test"
    );
    userEvent.click(
      screen.getByRole("button", {
        name: "profile.credentialsModal.form.edit",
      })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "profile.credentialsModal.alerts.editSuccess",
        "groupAlerts.titleSuccess"
      );
    });

    expect(handleOnClose).toHaveBeenCalledTimes(0);

    jest.clearAllMocks();
  });

  it("should update secrets in bulk", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnClose: jest.Mock = jest.fn();

    const mockQuery: MockedResponse[] = [
      {
        request: {
          query: GET_STAKEHOLDER_CREDENTIALS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              credentials: [
                {
                  __typename: "Credentials",
                  id: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
                  name: "Credentials test",
                  organization: {
                    __typename: "Organization",
                    id: "c966d57a-adde-43c3-bd47-1770002aa122",
                    name: "Organization name",
                  },
                  type: "HTTPS",
                },
                {
                  __typename: "Credentials",
                  id: "60f41b5e-7f48-443b-a6b1-7d004de4ac63",
                  name: "Credentials test 2",
                  organization: {
                    __typename: "Organization",
                    id: "c81b5dda-10ba-4350-ab60-d38c7f32bad8",
                    name: "Organization name 2",
                  },
                  type: "HTTPS",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_STAKEHOLDER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  id: "c966d57a-adde-43c3-bd47-1770002aa122",
                  name: "Organization name",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: UPDATE_CREDENTIALS,
          variables: {
            credentials: {
              password: "Password bulk",
              type: "HTTPS",
              user: "User bulk",
            },
            credentialsId: "60f41b5e-7f48-443b-a6b1-7d004de4ac63",
            organizationId: "c81b5dda-10ba-4350-ab60-d38c7f32bad8",
          },
        },
        result: { data: { updateCredentials: { success: true } } },
      },
      {
        request: {
          query: UPDATE_CREDENTIALS,
          variables: {
            credentials: {
              password: "Password bulk",
              type: "HTTPS",
              user: "User bulk",
            },
            credentialsId: "6e52c11c-abf7-4ca3-b7d0-635e394f41c1",
            organizationId: "c966d57a-adde-43c3-bd47-1770002aa122",
          },
        },
        result: { data: { updateCredentials: { success: true } } },
      },
    ];

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "front_can_edit_credentials_secrets_in_bulk" },
    ]);

    render(
      <MockedProvider
        addTypename={false}
        mocks={mockQuery.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <CredentialsModal onClose={handleOnClose} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.getByText("Credentials test")).toBeInTheDocument();
      expect(screen.getByText("Organization name")).toBeInTheDocument();
    });

    userEvent.click(
      screen.getByRole("button", {
        name: "profile.credentialsModal.actionButtons.editSecretsButton.text",
      })
    );
    userEvent.click(screen.getByText("profile.credentialsModal.form.https"));
    userEvent.type(screen.getByRole("textbox", { name: "user" }), "User bulk");
    userEvent.type(
      screen.getByRole("textbox", { name: "password" }),
      "Password bulk"
    );
    userEvent.click(screen.getAllByRole("checkbox")[0]);

    userEvent.click(
      screen.getByRole("button", {
        name: "profile.credentialsModal.form.edit",
      })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
      expect(msgSuccess).toHaveBeenLastCalledWith(
        "profile.credentialsModal.alerts.editSuccess",
        "groupAlerts.titleSuccess"
      );
    });

    expect(handleOnClose).toHaveBeenCalledTimes(0);

    jest.clearAllMocks();
  });
});
