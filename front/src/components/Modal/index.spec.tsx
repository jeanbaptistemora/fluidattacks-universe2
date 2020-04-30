import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { Button, ModalBody, ModalFooter, ModalHeader, ModalTitle } from "react-bootstrap";
import { Modal } from "./index";

const functionMock: (() => void) = (): void => undefined;

describe("Generic modal", () => {
  it("should return a function", () => {
    expect(typeof (Modal))
      .toEqual("function");
  });

  it("should render modal title", () => {
    const wrapper: ShallowWrapper = shallow(
      <Modal
        open={true}
        onClose={functionMock}
        headerTitle="Unit test title"
        footer={<div />}
      />,
    );
    expect(
      wrapper.contains(
        <ModalHeader className="header" closeLabel="Close" closeButton={false} bsClass="modal-header">
          <ModalTitle className="title" componentClass="h4">
            Unit test title
          </ModalTitle>
        </ModalHeader>,
    ))
      .toBeTruthy();
  });

  it("should render modal body", () => {
    const wrapper: ShallowWrapper = shallow(
      <Modal
        open={true}
        onClose={functionMock}
        headerTitle="Unit test title"
        content={<p>Unit modal content</p>}
        footer={<div />}
      />,
    );
    expect(
      wrapper.contains(
        <ModalBody componentClass="div">
          <p>
            Unit modal content
          </p>
        </ModalBody>,
    ))
      .toBeTruthy();
  });

  it("should render modal footer", () => {
    const wrapper: ShallowWrapper = shallow(
      <Modal
        open={true}
        onClose={functionMock}
        headerTitle="Unit test title"
        content={<p>Unit modal content</p>}
        footer={<Button>test btn</Button>}
      />,
    );
    expect(
      wrapper.contains(
        <ModalFooter componentClass="div">
          <Button active={false} block={false} disabled={false} bsStyle="default" bsClass="btn">
            test btn
          </Button>
        </ModalFooter>,
    ))
      .toBeTruthy();
  });

  it("should render a modal", () => {
    const wrapper: ShallowWrapper = shallow(
      <Modal
        open={true}
        onClose={functionMock}
        headerTitle="Unit test title"
        content={<p>Unit modal content</p>}
        footer={<Button>test btn</Button>}
      />,
    );
    expect(wrapper)
    .toHaveLength(1);
  });
});
