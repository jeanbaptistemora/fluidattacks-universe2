import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
import React from "react";

import { AddFilesModal } from "scenes/Dashboard/components/AddFilesModal";

describe("Add Files modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddFilesModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <AddFilesModal
        isOpen={true}
        isUploading={false}
        onClose={jest.fn()}
        onSubmit={jest.fn()}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render uploadbar", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <AddFilesModal
        isOpen={true}
        isUploading={true}
        onClose={jest.fn()}
        onSubmit={jest.fn()}
      />
    );

    expect(wrapper.text()).toMatch("Uploading file...");
  });

  it("should close on cancel", (): void => {
    expect.hasAssertions();

    const handleClose: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <AddFilesModal
        isOpen={true}
        isUploading={false}
        onClose={handleClose}
        onSubmit={jest.fn()}
      />
    );
    const cancelButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Cancel"))
      .at(0);
    cancelButton.simulate("click");

    expect(handleClose.mock.calls).toHaveLength(1);
  });
});
