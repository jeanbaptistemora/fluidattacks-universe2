import { MockedProvider } from "@apollo/react-testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";

import { DeleteGroup } from "scenes/Dashboard/containers/ProjectSettingsView/DeleteGroup";
import store from "store";

describe("DeleteGroup", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof DeleteGroup).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider>
          <MemoryRouter initialEntries={["/TEST"]}>
            <Route component={DeleteGroup} path={"/:projectName"} />
          </MemoryRouter>
        </MockedProvider>
      </Provider>
    );

    expect(wrapper).toHaveLength(1);
  });
});
