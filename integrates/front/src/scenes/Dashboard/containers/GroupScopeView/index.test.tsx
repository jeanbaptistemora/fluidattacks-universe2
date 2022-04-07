import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import {
  ACTIVATE_ROOT,
  ADD_GIT_ROOT,
  DEACTIVATE_ROOT,
  GET_ROOTS,
  UPDATE_GIT_ROOT,
} from "./queries";

import { GroupScopeView } from ".";
import { getCache } from "utils/apollo";
import { authContext } from "utils/auth";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

describe("GroupScopeView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupScopeView).toStrictEqual("function");
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
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                environmentUrls: [],
                gitignore: ["bower_components/*", "node_modules/*"],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: true,
                nickname: "product",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
                useVpn: false,
              },
            ],
          },
        },
      },
    };

    render(
      <authContext.Provider value={{ userEmail: "", userName: "" }}>
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
          "https://gitlab.com/fluidattacks/product",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
        ].join("")
      );
    });
  });

  it("should add git roots", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: { __typename: "Group", name: "unittesting", roots: [] },
        },
      },
    };
    const mutationMock: MockedResponse = {
      request: {
        query: ADD_GIT_ROOT,
        variables: {
          branch: "master",
          credentials: null,
          environment: "production",
          gitignore: [],
          groupName: "unittesting",
          includesHealthCheck: false,
          nickname: "",
          url: "https://gitlab.com/fluidattacks/product",
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
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                environmentUrls: [],
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                nickname: "product",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
                useVpn: false,
              },
            ],
          },
        },
      },
    };

    render(
      <authContext.Provider value={{ userEmail: "", userName: "" }}>
        <authzGroupContext.Provider
          value={
            new PureAbility([
              { action: "has_service_white" },
              { action: "is_continuous" },
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

    await waitFor((): void => {
      expect(screen.queryByText("group.scope.common.add")).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("group.scope.common.add"));

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "url" })
      ).toBeInTheDocument();
    });

    expect(screen.getByText("confirmmodal.proceed")).toBeDisabled();

    userEvent.type(
      screen.getByRole("textbox", { name: "url" }),
      "https://gitlab.com/fluidattacks/product"
    );
    userEvent.type(screen.getByRole("textbox", { name: "branch" }), "master");
    userEvent.type(
      screen.getByRole("textbox", { name: "environment" }),
      "production"
    );
    userEvent.click(screen.getByRole("radio", { name: "No" }));
    const numberOfRejectionCheckbox: number = 4;
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { checked: false })
      ).toHaveLength(numberOfRejectionCheckbox);
    });
    userEvent.click(
      screen.getByRole("checkbox", { name: "rejectHealthCheckA" })
    );
    userEvent.click(
      screen.getByRole("checkbox", { name: "rejectHealthCheckB" })
    );
    userEvent.click(
      screen.getByRole("checkbox", { name: "rejectHealthCheckC" })
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
        numberOfRejectionCheckbox - 1
      );
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
        [
          // Url
          "https://gitlab.com/fluidattacks/product",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
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
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                environmentUrls: [],
                gitignore: ["bower_components/*"],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                nickname: "product",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
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
          nickname: "product",
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
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "staging",
                environmentUrls: [],
                gitignore: ["node_modules/*"],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: true,
                nickname: "product",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
                useVpn: false,
              },
            ],
          },
        },
      },
    };

    render(
      <authContext.Provider value={{ userEmail: "", userName: "" }}>
        <authzGroupContext.Provider
          value={
            new PureAbility([
              { action: "has_service_white" },
              { action: "is_continuous" },
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

    userEvent.click(screen.queryAllByRole("row")[1]);
    await waitFor((): void => {
      expect(screen.getByText("group.scope.common.edit")).toBeInTheDocument();
    });

    expect(screen.getByText("confirmmodal.proceed")).toBeDisabled();

    userEvent.clear(screen.getByRole("textbox", { name: "environment" }));
    userEvent.type(
      screen.getByRole("textbox", { name: "environment" }),
      "staging"
    );
    userEvent.click(screen.getByRole("radio", { name: "Yes" }));
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { checked: false })
      ).toHaveLength(2);
    });
    userEvent.click(
      screen.getByRole("checkbox", { name: "includesHealthCheckA" })
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
        1
      );
    });
    userEvent.clear(screen.getByRole("textbox", { name: "gitignore[0]" }));
    userEvent.type(
      screen.getByRole("textbox", { name: "gitignore[0]" }),
      "node_modules/*"
    );
    await waitFor((): void => {
      expect(screen.getByText("confirmmodal.proceed")).not.toBeDisabled();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
        [
          // Url
          "https://gitlab.com/fluidattacks/product",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
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
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                environmentUrls: [],
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                nickname: "product",
                state: "INACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
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
                credentials: {
                  __typename: "Credentials",
                  id: "",
                  name: "",
                  type: "",
                },
                environment: "production",
                environmentUrls: [],
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                nickname: "product",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
                useVpn: false,
              },
            ],
          },
        },
      },
    };

    render(
      <authContext.Provider value={{ userEmail: "", userName: "" }}>
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
    expect(
      screen.getByRole<HTMLInputElement>("checkbox").checked
    ).toStrictEqual(false);

    userEvent.click(screen.getByRole("checkbox"));
    await waitFor((): void => {
      expect(
        screen.queryByText("group.scope.common.confirm")
      ).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(
        screen.getByRole<HTMLInputElement>("checkbox").checked
      ).toStrictEqual(true);
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
                  credentials: {
                    __typename: "Credentials",
                    id: "",
                    name: "",
                    type: "",
                  },
                  environment: "production",
                  environmentUrls: [],
                  gitignore: [],
                  id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: false,
                  nickname: "product",
                  state: "ACTIVE",
                  url: "https://gitlab.com/fluidattacks/product",
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
                  credentials: {
                    __typename: "Credentials",
                    id: "",
                    name: "",
                    type: "",
                  },
                  environment: "production",
                  environmentUrls: [],
                  gitignore: [],
                  id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: false,
                  nickname: "product",
                  state: "INACTIVE",
                  url: "https://gitlab.com/fluidattacks/product",
                  useVpn: false,
                },
              ],
            },
          },
        },
      };

      render(
        <authContext.Provider value={{ userEmail: "", userName: "" }}>
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "has_service_white" },
                { action: "is_continuous" },
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
      expect(
        screen.getByRole<HTMLInputElement>("checkbox").checked
      ).toStrictEqual(true);

      userEvent.click(screen.getByRole("checkbox"));
      await waitFor((): void => {
        expect(
          screen.queryByText("group.scope.common.deactivation.title")
        ).toBeInTheDocument();
      });

      expect(screen.getByText("confirmmodal.proceed")).toBeDisabled();

      userEvent.selectOptions(
        screen.getByRole("combobox", { name: "reason" }),
        [reason]
      );
      await waitFor((): void => {
        expect(screen.getByText("confirmmodal.proceed")).not.toBeDisabled();
      });

      expect(
        screen.queryByText("group.scope.common.confirm")
      ).not.toBeInTheDocument();

      userEvent.click(screen.getByText("confirmmodal.proceed"));
      await waitFor((): void => {
        expect(
          screen.queryByText("group.scope.common.confirm")
        ).toBeInTheDocument();
      });
      userEvent.click(screen.getAllByText("confirmmodal.proceed")[1]);
      await waitFor((): void => {
        expect(
          screen.getByRole<HTMLInputElement>("checkbox").checked
        ).toStrictEqual(false);
      });
    }
  );
});
