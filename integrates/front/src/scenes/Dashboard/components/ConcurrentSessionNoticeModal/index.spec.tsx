import { ConcurrentSessionNotice } from "scenes/Dashboard/components/ConcurrentSessionNoticeModal";
import React from "react";
import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";

describe("Concurrent session notice modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ConcurrentSessionNotice).toStrictEqual("function");
  });

  it("should be rendered", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <ConcurrentSessionNotice onClick={jest.fn()} open={true} />
    );

    expect(wrapper).toHaveLength(1);
  });
});
