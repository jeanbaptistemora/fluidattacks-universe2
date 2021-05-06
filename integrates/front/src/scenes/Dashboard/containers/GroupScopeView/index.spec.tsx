import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { DeactivationModal } from "./deactivationModal";
import {
  ACTIVATE_ROOT,
  ADD_GIT_ROOT,
  DEACTIVATE_ROOT,
  GET_ROOTS,
  UPDATE_GIT_ROOT,
} from "./queries";

import { GroupScopeView } from ".";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { SwitchButton } from "components/SwitchButton";
import store from "store";
import { getCache } from "utils/apollo";
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
            __typename: "Project",
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
                environment: "production",
                environmentUrls: [],
                gitignore: ["bower_components/*", "node_modules/*"],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: true,
                lastCloningStatusUpdate: "2021-01-05T18:16:48",
                lastStateStatusUpdate: "2021-01-05T18:16:48",
                nickname: "product",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
              },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <authzGroupContext.Provider
        value={new PureAbility([{ action: "has_drills_white" }])}
      >
        <MemoryRouter initialEntries={["/orgs/okada/groups/unittesting/scope"]}>
          <MockedProvider cache={getCache()} mocks={[queryMock]}>
            <Provider store={store}>
              <Route
                component={GroupScopeView}
                path={"/orgs/:organizationName/groups/:projectName/scope"}
              />
            </Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzGroupContext.Provider>
    );

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const firstTableRow: ReactWrapper = wrapper.find("tr").at(1);

    expect(firstTableRow.text()).toStrictEqual(
      [
        // Url
        "https://gitlab.com/fluidattacks/product",
        // Branch
        "master",
        // Exclude
        "bower_components/*",
        "node_modules/*",
        // State
        "Active",
        // Cloning status
        "Unknown",
        // Last cloning status update
        "2021-01-05 06:16:48",
      ].join("")
    );
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
          group: { __typename: "Project", name: "unittesting", roots: [] },
        },
      },
    };
    const mutationMock: MockedResponse = {
      request: {
        query: ADD_GIT_ROOT,
        variables: {
          branch: "master",
          environment: "production",
          gitignore: [],
          groupName: "unittesting",
          includesHealthCheck: false,
          nickname: "",
          url: "https://gitlab.com/fluidattacks/product",
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
            __typename: "Project",
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
                environment: "production",
                environmentUrls: [],
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastCloningStatusUpdate: "2021-01-05T18:16:48",
                lastStateStatusUpdate: "2021-01-05T18:16:48",
                nickname: "product",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
              },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "has_drills_white" }])}
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "backend_api_mutations_add_git_root_mutate" },
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
                  path={"/orgs/:organizationName/groups/:projectName/scope"}
                />
              </MockedProvider>
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </Provider>
    );

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const addButton: ReactWrapper = wrapper.find("button").at(0);
    addButton.simulate("click");

    const url: ReactWrapper = wrapper.find({ name: "url" }).find("input");
    url.simulate("change", {
      target: { name: "url", value: "https://gitlab.com/fluidattacks/product" },
    });

    const branch: ReactWrapper = wrapper.find({ name: "branch" }).find("input");
    branch.simulate("change", { target: { name: "branch", value: "master" } });

    const environment: ReactWrapper = wrapper
      .find({ name: "environment" })
      .find("input");
    environment.simulate("change", {
      target: { name: "environment", value: "production" },
    });

    await act(
      async (): Promise<void> => {
        wrapper.find("form").simulate("submit");
        const delay: number = 50;
        await wait(delay);
        wrapper.update();
      }
    );

    const firstTableRow: ReactWrapper = wrapper.find("tr").at(1);

    expect(firstTableRow.text()).toStrictEqual(
      [
        // Url
        "https://gitlab.com/fluidattacks/product",
        // Branch
        "master",
        // State
        "Active",
        // Cloning status
        "Unknown",
        // Last cloning status update
        "2021-01-05 06:16:48",
      ].join("")
    );
  });

  // Temporarily disabled
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should update git roots", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Project",
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
                environment: "production",
                environmentUrls: [],
                gitignore: ["bower_components/*"],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastCloningStatusUpdate: "2021-01-05T18:16:48",
                lastStateStatusUpdate: "2021-01-05T18:16:48",
                nickname: "product",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
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
            __typename: "Project",
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
                environment: "staging",
                environmentUrls: [],
                gitignore: ["node_modules/*"],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: true,
                lastCloningStatusUpdate: "2021-01-05T18:16:48",
                lastStateStatusUpdate: "2021-01-05T18:16:48",
                nickname: "product",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
              },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "has_drills_white" }])}
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "backend_api_mutations_add_git_root_mutate" },
                { action: "backend_api_mutations_update_git_root_mutate" },
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
                  path={"/orgs/:organizationName/groups/:projectName/scope"}
                />
              </MockedProvider>
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </Provider>
    );

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );
    const getFirstTableRow: () => ReactWrapper = (): ReactWrapper =>
      wrapper.find("tr").at(1) as ReactWrapper;

    getFirstTableRow().find("td").at(0).simulate("click");

    const editButton: ReactWrapper = wrapper.find("button").at(1);
    editButton.simulate("click");

    const environment: ReactWrapper = wrapper
      .find({ name: "environment" })
      .find("input");
    environment.simulate("change", {
      target: { name: "environment", value: "staging" },
    });

    wrapper.find(SwitchButton).at(0).simulate("click");
    wrapper.update();
    const includesHealthCheck: ReactWrapper = wrapper
      .find({ name: "includesHealthCheck" })
      .find("input");
    includesHealthCheck.simulate("change", {
      currentTarget: { name: "includesHealthCheck", value: true },
    });

    const path1: ReactWrapper = wrapper
      .find({ name: "gitignore.0" })
      .find("input");
    path1.simulate("change", {
      target: { name: "gitignore.0", value: "node_modules/*" },
    });

    await act(
      async (): Promise<void> => {
        wrapper.find("form").simulate("submit");
        await wait(0);
        wrapper.update();
      }
    );
    await wait(0);

    expect(includesHealthCheck.prop("value")).toStrictEqual(true);
    expect(getFirstTableRow().text()).toStrictEqual(
      [
        // Url
        "https://gitlab.com/fluidattacks/product",
        // Branch
        "master",
        // Exclude
        "node_modules/*",
        // State
        "Active",
        // Cloning status
        "Unknown",
        // Last cloning status update
        "2021-01-05 06:16:48",
      ].join("")
    );
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
            __typename: "Project",
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
                environment: "production",
                environmentUrls: [],
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastCloningStatusUpdate: "2021-01-05T18:16:48",
                lastStateStatusUpdate: "2021-01-05T18:16:48",
                nickname: "product",
                state: "INACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
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
            __typename: "Project",
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
                environment: "production",
                environmentUrls: [],
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastCloningStatusUpdate: "2021-01-05T18:16:48",
                lastStateStatusUpdate: "2021-01-05T18:16:48",
                nickname: "product",
                state: "ACTIVE",
                url: "https://gitlab.com/fluidattacks/product",
              },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "has_drills_white" }])}
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "backend_api_mutations_update_root_state_mutate" },
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
                  path={"/orgs/:organizationName/groups/:projectName/scope"}
                />
              </MockedProvider>
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </Provider>
    );

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const getStateSwitch: () => ReactWrapper = (): ReactWrapper => {
      const firstTableRow: ReactWrapper = wrapper.find("tr").at(1);

      return firstTableRow.find("#rootSwitch").at(0) as ReactWrapper;
    };

    expect(getStateSwitch().prop("checked")).toStrictEqual(false);

    getStateSwitch().simulate("click");

    const proceedButton: ReactWrapper = wrapper
      .find(ConfirmDialog)
      .find(Button)
      .at(1);
    proceedButton.simulate("click");

    await act(
      async (): Promise<void> => {
        const delay: number = 50;
        await wait(delay);
        wrapper.update();
      }
    );

    expect(getStateSwitch().prop("checked")).toStrictEqual(true);
  });

  it.each(["OUT_OF_SCOPE", "REGISTERED_BY_MISTAKE"])(
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
              __typename: "Project",
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
                  environment: "production",
                  environmentUrls: [],
                  gitignore: [],
                  id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: false,
                  lastCloningStatusUpdate: "2021-01-05T18:16:48",
                  lastStateStatusUpdate: "2021-01-05T18:16:48",
                  nickname: "product",
                  state: "ACTIVE",
                  url: "https://gitlab.com/fluidattacks/product",
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
              __typename: "Project",
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
                  environment: "production",
                  environmentUrls: [],
                  gitignore: [],
                  id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: false,
                  lastCloningStatusUpdate: "2021-01-05T18:16:48",
                  lastStateStatusUpdate: "2021-01-05T18:16:48",
                  nickname: "product",
                  state: "INACTIVE",
                  url: "https://gitlab.com/fluidattacks/product",
                },
              ],
            },
          },
        },
      };

      const wrapper = mount(
        <Provider store={store}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "has_drills_white" }])}
          >
            <authzPermissionsContext.Provider
              value={
                new PureAbility([
                  { action: "backend_api_mutations_update_root_state_mutate" },
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
                    path={"/orgs/:organizationName/groups/:projectName/scope"}
                  />
                </MockedProvider>
              </MemoryRouter>
            </authzPermissionsContext.Provider>
          </authzGroupContext.Provider>
        </Provider>
      );

      await act(
        async (): Promise<void> => {
          await wait(0);
          wrapper.update();
        }
      );

      const getStateSwitch = (): ReactWrapper => {
        const firstTableRow = wrapper.find("tr").at(1);

        return firstTableRow.find("#rootSwitch").at(0) as ReactWrapper;
      };

      expect(getStateSwitch().prop("checked")).toStrictEqual(true);

      getStateSwitch().simulate("click");

      const form = wrapper.find(DeactivationModal).find("form");

      form.find("select").simulate("change", {
        target: { name: "reason", value: reason },
      });

      form.simulate("submit");

      await act(
        async (): Promise<void> => {
          const delay: number = 50;
          await wait(delay);
          wrapper.update();
        }
      );

      expect(getStateSwitch().prop("checked")).toStrictEqual(false);
    }
  );
});
