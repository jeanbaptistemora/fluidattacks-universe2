import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { GroupSettingsView } from "scenes/Dashboard/containers/GroupSettingsView";
import { GET_TAGS } from "scenes/Dashboard/containers/GroupSettingsView/queries";
import store from "store";

describe("GroupSettingsView", (): void => {
  const mocksTags: Readonly<MockedResponse> = {
    request: {
      query: GET_TAGS,
      variables: {
        groupName: "TEST",
      },
    },
    result: {
      data: {
        group: {
          name: "TEST",
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
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupSettingsView).toStrictEqual("function");
  });

  it("should render tags component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={[mocksTags]}>
          <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
            <Route
              component={GroupSettingsView}
              path={"/orgs/:organizationName/groups/:groupName/scope"}
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
              component={GroupSettingsView}
              path={"/orgs/:organizationName/groups/:groupName/scope"}
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
              component={GroupSettingsView}
              path={"/orgs/:organizationName/groups/:groupName/scope"}
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
