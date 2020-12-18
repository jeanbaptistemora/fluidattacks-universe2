import { MockedProvider } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import * as React from "react";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { ProjectContent } from "scenes/Dashboard/containers/ProjectContent";
import store from "store";

describe("ProjectContent", () => {
  it("should return a function", () => {
    expect(typeof (ProjectContent))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    (window as typeof window & { userEmail: string }).userEmail = "test@test.com";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <Provider store={store}>
          <MockedProvider mocks={[]} addTypename={false}>
            <Route path={"/project/:projectName/indicators"} component={ProjectContent} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a component", async () => {
    (window as typeof window & { userEmail: string }).userEmail = "test@test.com";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <Provider store={store}>
          <MockedProvider mocks={[]} addTypename={false}>
            <Route path={"/project/:projectName/indicators"} component={ProjectContent}/>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
