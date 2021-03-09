import { MockedProvider } from "@apollo/react-testing";
import { ProjectContent } from "scenes/Dashboard/containers/ProjectContent";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import store from "store";
import wait from "waait";
import { MemoryRouter, Route } from "react-router-dom";

describe("ProjectContent", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ProjectContent).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={[]}>
            <Route
              component={ProjectContent}
              path={"/project/:projectName/indicators"}
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
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={[]}>
            <Route
              component={ProjectContent}
              path={"/project/:projectName/indicators"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });
});
