import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { Modal } from "components/Modal";

describe("Modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Modal).toStrictEqual("function");
  });

  it("should render modal title", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Modal headerTitle={"Unit test title"} open={true}>
        <p>{"Unit modal content"}</p>
      </Modal>
    );

    expect(wrapper.text()).toContain("Unit test title");
  });

  it("should render modal body", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Modal headerTitle={"Unit test title"} open={true}>
        <p>{"Unit modal content"}</p>
      </Modal>
    );

    expect(wrapper.text()).toContain("Unit modal content");
  });

  it("should render a modal", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Modal headerTitle={"Unit test title"} open={true}>
        <p>{"Unit modal content"}</p>
      </Modal>
    );

    expect(wrapper).toHaveLength(1);
  });
});
