import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";

import { MemoryRouter, Route } from "react-router";
import { ProjectSettingsView } from "scenes/Dashboard/containers/ProjectSettingsView";
import {
  GET_ENVIRONMENTS,
  GET_TAGS,
} from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";

describe("ProjectSettingsView", () => {
  const mocksTags: Readonly<MockedResponse> = {
      request: {
        query: GET_TAGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            tags: ["test"],
          },
        },
      },
  };

  const mocksEnvironments: Readonly<MockedResponse> = {
      request: {
        query: GET_ENVIRONMENTS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            environments: JSON.stringify([{
              urlEnv: "https://gitlab.com/fluidattacks/integrates",
            }]),
          },
        },
      },
  };

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_TAGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (ProjectSettingsView))
      .toEqual("function");
  });

  it("should render tags component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocksTags]} addTypename={false}>
          <MemoryRouter
            initialEntries={["/orgs/okada/groups/TEST/scope"]}
          >
            <Route
              component={ProjectSettingsView}
              path={"/orgs/:organizationName/groups/:projectName/scope"}
            />
          </MemoryRouter>
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render environments component", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_update_environment" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocksEnvironments]} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <MemoryRouter
              initialEntries={["/orgs/okada/groups/TEST/scope"]}
            >
              <Route
                component={ProjectSettingsView}
                path={"/orgs/:organizationName/groups/:projectName/scope"}
              />
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(200); wrapper.update(); });
    const onerow: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell");
    const statuschecked: boolean | undefined = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(2)
      .find("e")
      .prop("checked");
    expect(wrapper)
      .toHaveLength(1);
    expect(onerow)
      .toHaveLength(3);
    expect(statuschecked)
      .toEqual(true || false);
  });

  it("should render a error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={false}>
          <MemoryRouter
            initialEntries={["/orgs/okada/groups/TEST/scope"]}
          >
            <Route
              component={ProjectSettingsView}
              path={"/orgs/:organizationName/groups/:projectName/scope"}
            />
          </MemoryRouter>
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render files component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocksTags]} addTypename={false}>
          <MemoryRouter
            initialEntries={["/orgs/okada/groups/TEST/scope"]}
          >
            <Route
              component={ProjectSettingsView}
              path={"/orgs/:organizationName/groups/:projectName/scope"}
            />
          </MemoryRouter>
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper.find("#tblFiles"))
      .toBeTruthy();
  });
});
