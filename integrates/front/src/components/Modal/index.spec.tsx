/* eslint-disable react/forbid-component-props
  --------
  Disable for testing purposes
*/
import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { ModalBody, ModalHeader, ModalTitle } from "./styles";

import { Modal } from "components/Modal";

describe("Generic modal", (): void => {
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

    expect(
      wrapper.contains(
        <ModalHeader>
          <ModalTitle>{"Unit test title"}</ModalTitle>
        </ModalHeader>
      )
    ).toBe(true);
  });

  it("should render modal body", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Modal headerTitle={"Unit test title"} open={true}>
        <p>{"Unit modal content"}</p>
      </Modal>
    );

    expect(
      wrapper.contains(
        <ModalBody>
          <p>{"Unit modal content"}</p>
        </ModalBody>
      )
    ).toBe(true);
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
