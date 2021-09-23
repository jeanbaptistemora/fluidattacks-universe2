import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { GroupContent } from "scenes/Dashboard/containers/GroupContent";

describe("GroupContent", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupContent).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/test/vulns"]}>
        <MockedProvider addTypename={false} mocks={[]}>
          <Route
            component={GroupContent}
            path={"/orgs/:organizationName/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  // Exception: WF(This function must contain explicit assert)
  // eslint-disable-next-line
  it("should render a component", async (): Promise<void> => { // NOSONAR
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/test/vulns"]}>
        <MockedProvider addTypename={false} mocks={[]}>
          <Route
            component={GroupContent}
            path={"/orgs/:organizationName/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });
});
