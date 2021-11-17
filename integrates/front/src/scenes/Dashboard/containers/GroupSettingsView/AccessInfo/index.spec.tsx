import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { AccessInfo } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo";

describe("AccessInfo", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof AccessInfo).toStrictEqual("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider>
        <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
          <Route
            component={AccessInfo}
            path={"/orgs/:organizationName/groups/:groupName/scope"}
          />
        </MemoryRouter>
      </MockedProvider>
    );

    expect(wrapper).toHaveLength(1);
  });
});
