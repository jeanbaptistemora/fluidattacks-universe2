import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
import React from "react";

import { AddFilesBasicModal } from "scenes/Dashboard/components/AddFilesBasicModal";

describe("Add Files modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddFilesBasicModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <AddFilesBasicModal
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
      <AddFilesBasicModal
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
      <AddFilesBasicModal
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
