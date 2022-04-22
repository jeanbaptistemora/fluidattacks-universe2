import { render, screen } from "@testing-library/react";
import React from "react";

import { Modal } from "components/Modal";

describe("Modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Modal).toBe("function");
  });

  it("should render modal title", (): void => {
    expect.hasAssertions();

    render(
      <Modal open={true} title={"Unit test title"}>
        <p>{"Unit modal content"}</p>
      </Modal>
    );

    expect(screen.queryByText("Unit test title")).toBeInTheDocument();
  });

  it("should render modal body", (): void => {
    expect.hasAssertions();

    render(
      <Modal open={true} title={"Unit test title"}>
        <p>{"Unit modal content"}</p>
      </Modal>
    );

    expect(screen.queryByText("Unit modal content")).toBeInTheDocument();
  });

  it("should render a modal", (): void => {
    expect.hasAssertions();

    render(
      <Modal open={true} title={"Unit test title"}>
        <p>{"Unit modal content"}</p>
      </Modal>
    );

    expect(screen.queryByText("Unit modal content")).toBeInTheDocument();
    expect(screen.queryByText("Unit test title")).toBeInTheDocument();
  });
});
