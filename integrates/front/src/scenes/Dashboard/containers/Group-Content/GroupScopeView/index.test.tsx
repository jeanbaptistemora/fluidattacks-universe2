import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupScopeView } from "scenes/Dashboard/containers/Group-Content/GroupScopeView";
import {
  ACTIVATE_ROOT,
  ADD_GIT_ROOT,
  DEACTIVATE_ROOT,
  GET_ROOTS,
  UPDATE_GIT_ROOT,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/queries";
import { getCache } from "utils/apollo";
import { authContext } from "utils/auth";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

describe("GroupScopeView", (): void => {
  const btnConfirm = "components.modal.confirm";

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupScopeView).toBe("function");
  });

  it("should render git roots", async (): Promise<void> => {
    expect.hasAssertions();

    const queryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                cloningStatus: {
                  __typename: "GitRootCloningStatus",
                  message: "root created",
                  status: "UNKNOWN",
                },
                createdAt: "2022-02-10T14:58:10+00:00",
                createdBy: "testuser1@test.test",
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                gitEnvironmentUrls: [],
                gitignore: ["bower_components/*", "node_modules/*"],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: true,
                lastEditedAt: "2022-10-21T15:58:31+00:00",
                lastEditedBy: "testuser2@test.test",
                nickname: "universe",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/universe",
                useVpn: false,
              },
            ],
          },
        },
      },
    };

    render(
      <authContext.Provider
        value={{
          tours: {
            newGroup: true,
            newRiskExposure: true,
            newRoot: true,
            welcome: true,
          },
          userEmail: "",
          userName: "",
        }}
      >
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "has_service_white" }])}
        >
          <MemoryRouter
            initialEntries={["/orgs/okada/groups/unittesting/scope"]}
          >
            <MockedProvider cache={getCache()} mocks={[queryMock]}>
              <Route
                component={GroupScopeView}
                path={"/orgs/:organizationName/groups/:groupName/scope"}
              />
            </MockedProvider>
          </MemoryRouter>
        </authzGroupContext.Provider>
      </authContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("table.noDataIndication")
      ).not.toBeInTheDocument();
    });

    expect(screen.queryAllByRole("row")).toHaveLength(2);

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
        [
          // Url
          "https://gitlab.com/fluidattacks/universe",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
          // HealthCheck
          "group.scope.git.healthCheck.yes",
        ].join("")
      );
    });
  });

  it("should add git roots with token credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            roots: [],
          },
        },
      },
    };
    const mutationMock: MockedResponse = {
      request: {
        query: ADD_GIT_ROOT,
        variables: {
          branch: "master",
          credentials: {
            azureOrganization: "testorg1",
            isPat: true,
            key: undefined,
            name: "credential name",
            password: "",
            token: "token-test",
            type: "HTTPS",
            user: "",
          },
          environment: "production",
          gitignore: [],
          groupName: "unittesting",
          includesHealthCheck: false,
          nickname: "",
          url: "https://gitlab.com/fluidattacks/universe",
          useVpn: false,
        },
      },
      result: {
        data: { addGitRoot: { __typename: "SimplePayload", success: true } },
      },
    };
    const finalQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                cloningStatus: {
                  __typename: "GitRootCloningStatus",
                  message: "root created",
                  status: "UNKNOWN",
                },
                createdAt: "2022-02-10T14:58:10+00:00",
                createdBy: "testuser1@test.test",
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                gitEnvironmentUrls: [],
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastEditedAt: "2022-10-21T15:58:31+00:00",
                lastEditedBy: "testuser2@test.test",
                nickname: "universe",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/universe",
                useVpn: false,
              },
            ],
          },
        },
      },
    };

    render(
      <authContext.Provider
        value={{
          tours: {
            newGroup: true,
            newRiskExposure: true,
            newRoot: true,
            welcome: true,
          },
          userEmail: "",
          userName: "",
        }}
      >
        <authzGroupContext.Provider
          value={
            new PureAbility([
              { action: "has_service_white" },
              { action: "has_squad" },
            ])
          }
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_add_git_root_mutate" },
                { action: "api_mutations_add_secret_mutate" },
                { action: "api_mutations_update_git_root_mutate" },
              ])
            }
          >
            <MemoryRouter
              initialEntries={["/orgs/okada/groups/unittesting/scope"]}
            >
              <MockedProvider
                cache={getCache()}
                mocks={[initialQueryMock, mutationMock, finalQueryMock]}
              >
                <Route
                  component={GroupScopeView}
                  path={"/orgs/:organizationName/groups/:groupName/scope"}
                />
              </MockedProvider>
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </authContext.Provider>
    );

    await expect(
      screen.findByText("group.scope.common.add")
    ).resolves.toBeInTheDocument();

    await userEvent.click(screen.getByText("group.scope.common.add"));

    expect(screen.queryByRole("textbox", { name: "url" })).toBeInTheDocument();
    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.type(
      screen.getByRole("textbox", { name: "url" }),
      "https://gitlab.com/fluidattacks/universe"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "branch" }),
      "master"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "environment" }),
      "production"
    );

    expect(
      screen.getByRole("combobox", { name: "credentials.typeCredential" })
    ).toHaveValue("");

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "credentials.typeCredential" }),
      ["SSH"]
    );

    expect(
      screen.queryByRole("textbox", { name: "credentials.key" })
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.password" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.user" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.token" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.azureOrganization" })
    ).not.toBeInTheDocument();

    await userEvent.clear(
      screen.getByRole("textbox", { name: "credentials.name" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "credentials.name" }),
      "credential name"
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "credentials.typeCredential" }),
      ["USER"]
    );

    expect(
      screen.queryByRole("textbox", { name: "credentials.user" })
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.key" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.token" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.azureOrganization" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.password" })
    ).toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "credentials.typeCredential" }),
      ["TOKEN"]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "credentials.token" }),
      "token-test"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "credentials.azureOrganization" }),
      "testorg1"
    );

    await userEvent.click(screen.getByRole("radio", { name: "No" }));
    const numberOfRejectionCheckbox: number = 4;

    expect(screen.queryAllByRole("checkbox", { checked: false })).toHaveLength(
      numberOfRejectionCheckbox
    );

    await userEvent.click(screen.getByDisplayValue("rejectA"));
    await userEvent.click(screen.getByDisplayValue("rejectB"));
    await userEvent.click(screen.getByDisplayValue("rejectC"));

    expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
      numberOfRejectionCheckbox - 1
    );

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
        [
          // Url
          "https://gitlab.com/fluidattacks/universe",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
          // HealthCheck
          "group.scope.git.healthCheck.no",
        ].join("")
      );
    });
  });

  it("should add git roots with ssh credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            roots: [],
          },
        },
      },
    };
    const mutationMock: MockedResponse = {
      request: {
        query: ADD_GIT_ROOT,
        variables: {
          branch: "master",
          credentials: {
            azureOrganization: undefined,
            isPat: false,
            key: "LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KdGVzdAotLS0tLUVORCBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0=",
            name: "credential name",
            password: "",
            token: "",
            type: "SSH",
            user: "",
          },
          environment: "production",
          gitignore: [],
          groupName: "unittesting",
          includesHealthCheck: false,
          nickname: "",
          url: "https://gitlab.com/fluidattacks/universe",
          useVpn: false,
        },
      },
      result: {
        data: { addGitRoot: { __typename: "SimplePayload", success: true } },
      },
    };
    const finalQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                cloningStatus: {
                  __typename: "GitRootCloningStatus",
                  message: "root created",
                  status: "UNKNOWN",
                },
                createdAt: "2022-02-10T14:58:10+00:00",
                createdBy: "testuser1@test.test",
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                gitEnvironmentUrls: [],
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastEditedAt: "2022-10-21T15:58:31+00:00",
                lastEditedBy: "testuser2@test.test",
                nickname: "universe",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/universe",
                useVpn: false,
              },
            ],
          },
        },
      },
    };

    render(
      <authContext.Provider
        value={{
          tours: {
            newGroup: true,
            newRiskExposure: true,
            newRoot: true,
            welcome: true,
          },
          userEmail: "",
          userName: "",
        }}
      >
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "has_service_white" }])}
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_add_git_root_mutate" },
                { action: "api_mutations_add_secret_mutate" },
                { action: "api_mutations_update_git_root_mutate" },
              ])
            }
          >
            <MemoryRouter
              initialEntries={["/orgs/okada/groups/unittesting/scope"]}
            >
              <MockedProvider
                cache={getCache()}
                mocks={[initialQueryMock, mutationMock, finalQueryMock]}
              >
                <Route
                  component={GroupScopeView}
                  path={"/orgs/:organizationName/groups/:groupName/scope"}
                />
              </MockedProvider>
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </authContext.Provider>
    );

    await expect(
      screen.findByText("group.scope.common.add")
    ).resolves.toBeInTheDocument();

    await userEvent.click(screen.getByText("group.scope.common.add"));

    expect(screen.queryByRole("textbox", { name: "url" })).toBeInTheDocument();
    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.type(
      screen.getByRole("textbox", { name: "url" }),
      "https://gitlab.com/fluidattacks/universe"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "branch" }),
      "master"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "environment" }),
      "production"
    );

    expect(
      screen.getByRole("combobox", { name: "credentials.typeCredential" })
    ).toHaveValue("");

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "credentials.typeCredential" }),
      ["SSH"]
    );

    expect(
      screen.queryByRole("textbox", { name: "credentials.key" })
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.password" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.user" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.token" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.azureOrganization" })
    ).not.toBeInTheDocument();

    await userEvent.clear(
      screen.getByRole("textbox", { name: "credentials.name" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "credentials.name" }),
      "credential name"
    );
    await userEvent.clear(
      screen.getByRole("textbox", { name: "credentials.key" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "credentials.key" }),
      "-----BEGIN OPENSSH PRIVATE KEY-----\ntest\n-----END OPENSSH PRIVATE KEY-----"
    );

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
        [
          // Url
          "https://gitlab.com/fluidattacks/universe",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
          // HealthCheck
          "group.scope.git.healthCheck.no",
        ].join("")
      );
    });
  });

  it("should update git roots", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                cloningStatus: {
                  __typename: "GitRootCloningStatus",
                  message: "root created",
                  status: "UNKNOWN",
                },
                createdAt: "2022-02-10T14:58:10+00:00",
                createdBy: "testuser1@test.test",
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                gitEnvironmentUrls: [],
                gitignore: ["bower_components/*"],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastEditedAt: "2022-10-21T15:58:31+00:00",
                lastEditedBy: "testuser2@test.test",
                nickname: "universe",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/universe",
                useVpn: false,
              },
            ],
          },
        },
      },
    };
    const mutationMock: MockedResponse = {
      request: {
        query: UPDATE_GIT_ROOT,
        variables: {
          credentials: null,
          environment: "staging",
          gitignore: ["node_modules/*"],
          groupName: "unittesting",
          id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
          includesHealthCheck: true,
          nickname: "universe",
        },
      },
      result: {
        data: { updateGitRoot: { __typename: "SimplePayload", success: true } },
      },
    };
    const finalQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                cloningStatus: {
                  __typename: "GitRootCloningStatus",
                  message: "root created",
                  status: "UNKNOWN",
                },
                createdAt: "2022-02-10T14:58:10+00:00",
                createdBy: "testuser1@test.test",
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "staging",
                gitEnvironmentUrls: [],
                gitignore: ["node_modules/*"],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: true,
                lastEditedAt: "2022-10-21T15:58:31+00:00",
                lastEditedBy: "testuser2@test.test",
                nickname: "universe",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/universe",
                useVpn: false,
              },
            ],
          },
        },
      },
    };

    render(
      <authContext.Provider
        value={{
          tours: {
            newGroup: true,
            newRiskExposure: true,
            newRoot: true,
            welcome: true,
          },
          userEmail: "",
          userName: "",
        }}
      >
        <authzGroupContext.Provider
          value={
            new PureAbility([
              { action: "has_service_white" },
              { action: "has_squad" },
            ])
          }
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_add_git_root_mutate" },
                { action: "api_mutations_update_git_root_mutate" },
                { action: "update_git_root_filter" },
              ])
            }
          >
            <MemoryRouter
              initialEntries={["/orgs/okada/groups/unittesting/scope"]}
            >
              <MockedProvider
                cache={getCache()}
                mocks={[initialQueryMock, mutationMock, finalQueryMock]}
              >
                <Route
                  component={GroupScopeView}
                  path={"/orgs/:organizationName/groups/:groupName/scope"}
                />
              </MockedProvider>
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </authContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("table.noDataIndication")
      ).not.toBeInTheDocument();
    });

    expect(screen.queryAllByRole("row")).toHaveLength(2);

    await userEvent.click(screen.queryAllByRole("row")[1]);
    await waitFor((): void => {
      expect(screen.getByText("group.scope.common.edit")).toBeInTheDocument();
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.clear(screen.getByRole("textbox", { name: "environment" }));
    await userEvent.type(
      screen.getByRole("textbox", { name: "environment" }),
      "staging"
    );
    await userEvent.click(screen.getByRole("radio", { name: "Yes" }));
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { checked: false })
      ).toHaveLength(2);
    });
    await userEvent.click(screen.getByDisplayValue("includeA"));
    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
        1
      );
    });
    await userEvent.clear(
      screen.getByRole("textbox", { name: "gitignore[0]" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "gitignore[0]" }),
      "node_modules/*"
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
        [
          // Url
          "https://gitlab.com/fluidattacks/universe",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
          // HeathCheck
          "group.scope.git.healthCheck.no",
        ].join("")
      );
    });
  });

  it("should activate root", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                cloningStatus: {
                  __typename: "GitRootCloningStatus",
                  message: "root created",
                  status: "UNKNOWN",
                },
                createdAt: "2022-02-10T14:58:10+00:00",
                createdBy: "testuser1@test.test",
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                gitEnvironmentUrls: [],
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastEditedAt: "2022-10-21T15:58:31+00:00",
                lastEditedBy: "testuser2@test.test",
                nickname: "universe",
                state: "INACTIVE",
                url: "https://gitlab.com/fluidattacks/universe",
                useVpn: false,
              },
            ],
          },
        },
      },
    };
    const mutationMock: MockedResponse = {
      request: {
        query: ACTIVATE_ROOT,
        variables: {
          groupName: "unittesting",
          id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
        },
      },
      result: {
        data: {
          activateRoot: { __typename: "SimplePayload", success: true },
        },
      },
    };
    const finalQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                cloningStatus: {
                  __typename: "GitRootCloningStatus",
                  message: "root created",
                  status: "UNKNOWN",
                },
                createdAt: "2022-02-10T14:58:10+00:00",
                createdBy: "testuser1@test.test",
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                gitEnvironmentUrls: [],
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastEditedAt: "2022-10-21T15:58:31+00:00",
                lastEditedBy: "testuser2@test.test",
                nickname: "universe",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/universe",
                useVpn: false,
              },
            ],
          },
        },
      },
    };

    render(
      <authContext.Provider
        value={{
          tours: {
            newGroup: true,
            newRiskExposure: true,
            newRoot: true,
            welcome: true,
          },
          userEmail: "",
          userName: "",
        }}
      >
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "has_service_white" }])}
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_activate_root_mutate" },
              ])
            }
          >
            <MemoryRouter
              initialEntries={["/orgs/okada/groups/unittesting/scope"]}
            >
              <MockedProvider
                cache={getCache()}
                mocks={[initialQueryMock, mutationMock, finalQueryMock]}
              >
                <Route
                  component={GroupScopeView}
                  path={"/orgs/:organizationName/groups/:groupName/scope"}
                />
              </MockedProvider>
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </authContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("table.noDataIndication")
      ).not.toBeInTheDocument();
    });

    expect(screen.queryAllByRole("row")).toHaveLength(2);
    expect(
      screen.queryByText("group.scope.common.confirm")
    ).not.toBeInTheDocument();
    expect(screen.getByRole<HTMLInputElement>("checkbox").checked).toBe(false);

    await userEvent.click(screen.getByRole("checkbox"));
    await waitFor((): void => {
      expect(
        screen.queryByText("group.scope.common.confirm")
      ).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(screen.getByRole<HTMLInputElement>("checkbox").checked).toBe(true);
    });
  });

  it.each(["REGISTERED_BY_MISTAKE"])(
    "should deactivate root with reason %s",
    async (reason): Promise<void> => {
      expect.hasAssertions();

      const initialQueryMock: MockedResponse = {
        request: {
          query: GET_ROOTS,
          variables: { groupName: "unittesting" },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              name: "unittesting",
              roots: [
                {
                  __typename: "GitRoot",
                  branch: "master",
                  cloningStatus: {
                    __typename: "GitRootCloningStatus",
                    message: "root created",
                    status: "UNKNOWN",
                  },
                  createdAt: "2022-02-10T14:58:10+00:00",
                  createdBy: "testuser1@test.test",
                  credentials: {
                    __typename: "Credentials",
                    id: "",
                    name: "",
                    type: "",
                  },
                  environment: "production",
                  gitEnvironmentUrls: [],
                  gitignore: [],
                  id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: false,
                  lastEditedAt: "2022-10-21T15:58:31+00:00",
                  lastEditedBy: "testuser2@test.test",
                  nickname: "universe",
                  state: "ACTIVE",
                  url: "https://gitlab.com/fluidattacks/universe",
                  useVpn: false,
                },
              ],
            },
          },
        },
      };
      const mutationMock: MockedResponse = {
        request: {
          query: DEACTIVATE_ROOT,
          variables: {
            groupName: "unittesting",
            id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
            other: "",
            reason,
          },
        },
        result: {
          data: {
            deactivateRoot: { __typename: "SimplePayload", success: true },
          },
        },
      };
      const finalQueryMock: MockedResponse = {
        request: {
          query: GET_ROOTS,
          variables: { groupName: "unittesting" },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              name: "unittesting",
              roots: [
                {
                  __typename: "GitRoot",
                  branch: "master",
                  cloningStatus: {
                    __typename: "GitRootCloningStatus",
                    message: "root created",
                    status: "UNKNOWN",
                  },
                  createdAt: "2022-02-10T14:58:10+00:00",
                  createdBy: "testuser1@test.test",
                  credentials: {
                    __typename: "Credentials",
                    id: "",
                    name: "",
                    type: "",
                  },
                  environment: "production",
                  gitEnvironmentUrls: [],
                  gitignore: [],
                  id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: false,
                  lastEditedAt: "2022-10-21T15:58:31+00:00",
                  lastEditedBy: "testuser2@test.test",
                  nickname: "universe",
                  state: "INACTIVE",
                  url: "https://gitlab.com/fluidattacks/universe",
                  useVpn: false,
                },
              ],
            },
          },
        },
      };

      render(
        <authContext.Provider
          value={{
            tours: {
              newGroup: true,
              newRiskExposure: true,
              newRoot: true,
              welcome: true,
            },
            userEmail: "",
            userName: "",
          }}
        >
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "has_service_white" },
                { action: "has_squad" },
              ])
            }
          >
            <authzPermissionsContext.Provider
              value={
                new PureAbility([
                  { action: "api_mutations_activate_root_mutate" },
                ])
              }
            >
              <MemoryRouter
                initialEntries={["/orgs/okada/groups/unittesting/scope"]}
              >
                <MockedProvider
                  cache={getCache()}
                  mocks={[initialQueryMock, mutationMock, finalQueryMock]}
                >
                  <Route
                    component={GroupScopeView}
                    path={"/orgs/:organizationName/groups/:groupName/scope"}
                  />
                </MockedProvider>
              </MemoryRouter>
            </authzPermissionsContext.Provider>
          </authzGroupContext.Provider>
        </authContext.Provider>
      );

      await waitFor((): void => {
        expect(
          screen.queryByText("table.noDataIndication")
        ).not.toBeInTheDocument();
      });

      expect(screen.queryAllByRole("row")).toHaveLength(2);
      expect(
        screen.queryByText("group.scope.common.confirm")
      ).not.toBeInTheDocument();
      expect(screen.getByRole<HTMLInputElement>("checkbox").checked).toBe(true);

      await userEvent.click(screen.getByRole("checkbox"));
      await waitFor((): void => {
        expect(
          screen.queryByText("group.scope.common.deactivation.title")
        ).toBeInTheDocument();
      });

      expect(screen.getByText(btnConfirm)).toBeDisabled();

      await userEvent.selectOptions(
        screen.getByRole("combobox", { name: "reason" }),
        [reason]
      );
      await waitFor((): void => {
        expect(screen.getByText(btnConfirm)).not.toBeDisabled();
      });

      expect(
        screen.queryByText("group.scope.common.confirm")
      ).not.toBeInTheDocument();

      await userEvent.click(screen.getByText(btnConfirm));
      await waitFor((): void => {
        expect(
          screen.queryByText("group.scope.common.confirm")
        ).toBeInTheDocument();
      });
      await userEvent.click(screen.getAllByText(btnConfirm)[1]);
      await waitFor((): void => {
        expect(screen.getByRole<HTMLInputElement>("checkbox").checked).toBe(
          false
        );
      });
    }
  );
});
