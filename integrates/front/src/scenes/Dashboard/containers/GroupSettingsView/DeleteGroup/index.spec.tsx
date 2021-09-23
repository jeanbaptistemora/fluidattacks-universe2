import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { DeleteGroup } from "scenes/Dashboard/containers/GroupSettingsView/DeleteGroup";

describe("DeleteGroup", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof DeleteGroup).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider>
        <MemoryRouter initialEntries={["/TEST"]}>
          <Route component={DeleteGroup} path={"/:groupName"} />
        </MemoryRouter>
      </MockedProvider>
    );

    expect(wrapper).toHaveLength(1);
  });
});
