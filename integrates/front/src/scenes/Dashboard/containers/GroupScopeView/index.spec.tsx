import { GroupScopeView } from ".";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { Provider } from "react-redux";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { act } from "react-dom/test-utils";
import { cache } from "utils/apollo";
import { mount } from "enzyme";
import store from "store";
import wait from "waait";
import { ADD_GIT_ROOT, GET_ROOTS } from "./query";
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
          <MockedProvider cache={cache} mocks={[queryMock]}>
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

    const firstRowInfo: ReactWrapper = wrapper.find("RowPureContent").at(0);

    expect(firstRowInfo.text()).toStrictEqual(
      ["https://gitlab.com/fluidattacks/product", "master", "production"].join(
        ""
      )
    );
  });

  // Will be enabled next MR
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should add git roots", async (): Promise<void> => {
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
                cache={cache}
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

    wrapper.find("form").simulate("submit");

    await act(
      async (): Promise<void> => {
        const delay: number = 200;
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
});
