import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
import { Provider } from "react-redux";
import wait from "waait";

import { MemoryRouter, Route } from "react-router";
import { ProjectSettingsView } from "scenes/Dashboard/containers/ProjectSettingsView";
import { GET_TAGS } from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import store from "store";

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
