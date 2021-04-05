import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { Comments } from "scenes/Dashboard/components/Comments";

const functionMock: () => void = (): void => undefined;

describe("Comments Box", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Comments).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Comments
        id={"comments-test"}
        onLoad={functionMock}
        onPostComment={functionMock}
      />
    );

    expect(wrapper.contains(<div id={"comments-test"} />)).toBe(true);
  });
});
