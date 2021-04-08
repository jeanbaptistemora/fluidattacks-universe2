import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { ProjectContent } from "scenes/Dashboard/containers/ProjectContent";
import store from "store";

describe("ProjectContent", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ProjectContent).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/test/vulns"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={[]}>
            <Route
              component={ProjectContent}
              path={"/orgs/:organizationName/groups/:projectName/vulns"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/test/vulns"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={[]}>
            <Route
              component={ProjectContent}
              path={"/orgs/:organizationName/groups/:projectName/vulns"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });
});
