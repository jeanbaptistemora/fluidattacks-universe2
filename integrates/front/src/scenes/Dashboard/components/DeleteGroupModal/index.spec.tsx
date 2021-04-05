import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { DeleteGroupModal } from "scenes/Dashboard/components/DeleteGroupModal";

const functionMock: () => void = (): void => undefined;

describe("Delete Group Modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof DeleteGroupModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <DeleteGroupModal
        groupName={"TEST"}
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );

    expect(wrapper).toHaveLength(1);
  });
});
