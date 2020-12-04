import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { GroupScopeView } from ".";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { Provider } from "react-redux";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { SwitchButton } from "components/SwitchButton";
import { act } from "react-dom/test-utils";
import { getCache } from "utils/apollo";
import { mount } from "enzyme";
import store from "store";
import wait from "waait";
import {
  ADD_GIT_ROOT,
  GET_ROOTS,
  UPDATE_GIT_ROOT,
  UPDATE_ROOT_STATE,
} from "./query";
import { MemoryRouter, Route } from "react-router";
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
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                environment: "production",
                environmentUrls: [],
                filter: {
                  __typename: "GitRootFilter",
                  paths: ["^.*/bower_components/.*$", "^.*/node_modules/.*$"],
                  policy: "EXCLUDE",
                },
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: true,
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
      ["https://gitlab.com/fluidattacks/product", "master", "production"].join(
        ""
      )
    );
  });

  it("should add git roots", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: { data: { group: { __typename: "Project", roots: [] } } },
    };
    const mutationMock: MockedResponse = {
      request: {
        query: ADD_GIT_ROOT,
        variables: {
          branch: "master",
          environment: "production",
          filter: undefined,
          groupName: "unittesting",
          includesHealthCheck: false,
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
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                environment: "production",
                environmentUrls: [],
                filter: null,
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
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

    wrapper.find("button").simulate("click");
    const url: ReactWrapper = wrapper.find({ name: "url" }).find("input");
    url.simulate("change", {
      target: { value: "https://gitlab.com/fluidattacks/product" },
    });

    const branch: ReactWrapper = wrapper.find({ name: "branch" }).find("input");
    branch.simulate("change", { target: { value: "master" } });

    const environment: ReactWrapper = wrapper
      .find({ name: "environment" })
      .find("input");
    environment.simulate("change", { target: { value: "production" } });

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
      ["https://gitlab.com/fluidattacks/product", "master", "production"].join(
        ""
      )
    );
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
            __typename: "Project",
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                environment: "production",
                environmentUrls: [],
                filter: null,
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
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
          filter: { paths: ["node_modules/"], policy: "EXCLUDE" },
          id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
          includesHealthCheck: true,
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
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                environment: "staging",
                environmentUrls: [],
                filter: {
                  __typename: "GitRootFilter",
                  paths: ["node_modules/"],
                  policy: "EXCLUDE",
                },
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: true,
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
    const getfirstTableRow: () => ReactWrapper = (): ReactWrapper =>
      wrapper.find("tr").at(1) as ReactWrapper;

    getfirstTableRow().simulate("click");

    const environment: ReactWrapper = wrapper
      .find({ name: "environment" })
      .find("input");
    environment.simulate("change", { target: { value: "staging" } });

    wrapper.find(SwitchButton).at(0).simulate("click");
    wrapper.find(SwitchButton).at(1).simulate("click");

    const includesHealthCheck: ReactWrapper = wrapper
      .find({ name: "includesHealthCheck" })
      .find("input");
    includesHealthCheck.simulate("change", { target: { value: true } });

    const policy: ReactWrapper = wrapper
      .find({ name: "filter.policy" })
      .find("select");
    policy.simulate("change", { target: { value: "EXCLUDE" } });

    const path1: ReactWrapper = wrapper
      .find({ name: "filter.paths[0]" })
      .find("input");
    path1.simulate("change", { target: { value: "node_modules/" } });

    await act(
      async (): Promise<void> => {
        wrapper.find("form").simulate("submit");
        const delay: number = 50;
        await wait(delay);
        wrapper.update();
      }
    );

    expect(getfirstTableRow().text()).toStrictEqual(
      ["https://gitlab.com/fluidattacks/product", "master", "staging"].join("")
    );
  });

  // Will enable next MR
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should update root state", async (): Promise<void> => {
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
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                environment: "production",
                environmentUrls: [],
                filter: null,
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
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
        query: UPDATE_ROOT_STATE,
        variables: {
          id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
          state: "INACTIVE",
        },
      },
      result: {
        data: {
          updateRootState: { __typename: "SimplePayload", success: true },
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
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                environment: "production",
                environmentUrls: [],
                filter: null,
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                state: "INACTIVE",
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
    const getfirstTableRow: () => ReactWrapper = (): ReactWrapper =>
      wrapper.find("tr").at(1) as ReactWrapper;

    const stateSwitch: ReactWrapper = getfirstTableRow().find("td").last();
    stateSwitch.simulate("click");

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

    expect(getfirstTableRow().text()).toStrictEqual(
      [
        "https://gitlab.com/fluidattacks/product",
        "master",
        "production",
        "Inactive",
      ].join("")
    );
  });
});
