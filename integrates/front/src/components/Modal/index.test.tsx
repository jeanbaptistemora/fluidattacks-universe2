import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { Modal } from ".";

describe("Modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Modal).toBe("function");
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

  it("should call onClose after click button", async (): Promise<void> => {
    expect.hasAssertions();

    const handleClose: jest.Mock = jest.fn();
    const user = userEvent.setup();
    render(
      <Modal onClose={handleClose} open={true} title={"Unit test title"}>
        <p>{"Unit 2 modal content"}</p>
      </Modal>
    );

    await user.click(screen.getByRole("button"));
    await waitFor((): void => {
      expect(handleClose).toHaveBeenCalledTimes(1);
    });
  });

  it("should call onClose after press esc", async (): Promise<void> => {
    expect.hasAssertions();

    const handleClose: jest.Mock = jest.fn();
    const { container } = render(
      <Modal onClose={handleClose} open={true} title={"Unit test title"}>
        <p>{"Unit 2 modal content"}</p>
      </Modal>
    );

    fireEvent.keyDown(container, { key: "Escape" });
    await waitFor((): void => {
      expect(handleClose).toHaveBeenCalledTimes(1);
    });
  });
});
