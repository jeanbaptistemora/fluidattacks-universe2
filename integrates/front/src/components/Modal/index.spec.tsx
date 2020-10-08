/* eslint-disable react/forbid-component-props
  --------
  Disable for testing purposes
*/
import { Button } from "react-bootstrap";
import { Modal } from "components/Modal";
import React from "react";
import {
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
} from "styles/styledComponents";
import { ShallowWrapper, shallow } from "enzyme";

describe("Generic modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Modal).toStrictEqual("function");
  });

  it("should render modal title", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Modal
        footer={<div />}
        headerTitle={"Unit test title"}
        onClose={jest.fn()}
        open={true}
      />
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
      <Modal
        footer={<div />}
        headerTitle={"Unit test title"}
        onClose={jest.fn()}
        open={true}
      >
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

  it("should render modal footer", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Modal
        footer={<Button>{"test btn"}</Button>}
        headerTitle={"Unit test title"}
        onClose={jest.fn()}
        open={true}
      >
        <p>{"Unit modal content"}</p>
      </Modal>
    );

    expect(
      wrapper.contains(
        <ModalFooter>
          <Button
            active={false}
            block={false}
            bsClass={"btn"}
            bsStyle={"default"}
            disabled={false}
          >
            {"test btn"}
          </Button>
        </ModalFooter>
      )
    ).toBe(true);
  });

  it("should render a modal", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Modal
        footer={<Button>{"test btn"}</Button>}
        headerTitle={"Unit test title"}
        onClose={jest.fn()}
        open={true}
      >
        <p>{"Unit modal content"}</p>
      </Modal>
    );

    expect(wrapper).toHaveLength(1);
  });
});
