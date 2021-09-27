import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
import React from "react";

import { AddedFileModal } from "scenes/Dashboard/components/AddedFileModal";

describe("Added File modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddedFileModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <AddedFileModal isOpen={true} onClose={jest.fn()} />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should close on close", (): void => {
    expect.hasAssertions();

    const handleClose: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <AddedFileModal isOpen={true} onClose={handleClose} />
    );
    const cancelButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Close"))
      .at(0);
    cancelButton.simulate("click");

    expect(handleClose.mock.calls).toHaveLength(1);
  });
});
