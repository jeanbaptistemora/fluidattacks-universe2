import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
import React from "react";

import { AddTagsModal } from "scenes/Dashboard/components/AddTagsModal";

const functionMock: () => void = (): void => undefined;

describe("Add Tags modal", (): void => {
  const wrapper: ShallowWrapper = shallow(
    <AddTagsModal
      isOpen={true}
      onClose={functionMock}
      onSubmit={functionMock}
    />
  );

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddTagsModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();
    expect(wrapper).toHaveLength(1);
  });

  it("should render input field and add button", (): void => {
    expect.hasAssertions();

    const modal: ReactWrapper = mount(
      <AddTagsModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );

    const addButton: ReactWrapper = modal
      .find("FormikArrayField")
      .find("FontAwesomeIcon");

    const inputField: ReactWrapper = modal
      .find("FormikArrayField")
      .find("input");

    expect(addButton).toHaveLength(1);

    expect(inputField).toHaveLength(1);
  });

  it("should add and remove a input field", (): void => {
    expect.hasAssertions();

    const modal: ReactWrapper = mount(
      <AddTagsModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );
    const addButton: ReactWrapper = modal
      .find("FormikArrayField")
      .find(".fa-plus");

    addButton.simulate("click");

    expect(modal.find("FormikArrayField").find("input")).toHaveLength(2);

    const deleteButton: ReactWrapper = modal
      .find("FormikArrayField")
      .find(".fa-trash-alt");

    deleteButton.simulate("click");

    expect(modal.find("FormikArrayField").find("input")).toHaveLength(1);
  });
});
