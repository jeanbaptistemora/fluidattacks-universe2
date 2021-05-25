import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { Sidebar } from "scenes/Dashboard/components/Sidebar";

describe("Sidebar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Sidebar).toStrictEqual("function");
  });

  it("should render a sidebar", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <MemoryRouter initialEntries={["/home"]}>
        <Sidebar isLoading={false} />
      </MemoryRouter>
    );

    expect(wrapper).toHaveLength(1);
  });
});
