/* eslint-disable react/forbid-component-props
  --------
  Disable for testing purposes
*/
import { Modal } from ".";
import React from "react";
import {
  Button,
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
} from "react-bootstrap";
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
        <ModalHeader
          bsClass={"modal-header"}
          className={"header"}
          closeButton={false}
          closeLabel={"Close"}
        >
          <ModalTitle className={"title"} componentClass={"h4"}>
            {"Unit test title"}
          </ModalTitle>
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
        <ModalBody componentClass={"div"}>
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
        <ModalFooter componentClass={"div"}>
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
