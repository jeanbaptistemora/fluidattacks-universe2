import { DeleteGroup } from "scenes/Dashboard/containers/ProjectSettingsView/DeleteGroup";
import { MockedProvider } from "@apollo/react-testing";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import store from "store";
import { MemoryRouter, Route } from "react-router-dom";

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
