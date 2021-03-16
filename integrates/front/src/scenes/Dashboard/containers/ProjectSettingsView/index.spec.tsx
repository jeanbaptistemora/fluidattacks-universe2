import { GET_TAGS } from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import { GraphQLError } from "graphql";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { ProjectSettingsView } from "scenes/Dashboard/containers/ProjectSettingsView";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import store from "store";
import wait from "waait";
import { MemoryRouter, Route } from "react-router";

describe("ProjectSettingsView", (): void => {
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

  const mockError: readonly MockedResponse[] = [
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

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ProjectSettingsView).toStrictEqual("function");
  });

  it("should render tags component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={[mocksTags]}>
          <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
            <Route
              component={ProjectSettingsView}
              path={"/orgs/:organizationName/groups/:projectName/scope"}
            />
          </MemoryRouter>
        </MockedProvider>
      </Provider>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should render a error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
            <Route
              component={ProjectSettingsView}
              path={"/orgs/:organizationName/groups/:projectName/scope"}
            />
          </MemoryRouter>
        </MockedProvider>
      </Provider>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should render files component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={[mocksTags]}>
          <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
            <Route
              component={ProjectSettingsView}
              path={"/orgs/:organizationName/groups/:projectName/scope"}
            />
          </MemoryRouter>
        </MockedProvider>
      </Provider>
    );
    await wait(0);

    // eslint-disable-next-line jest/no-restricted-matchers
    expect(wrapper.find("#tblFiles")).toBeTruthy();
  });
});
