import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { AddTagsModal } from "scenes/Dashboard/components/AddTagsModal";

const functionMock: () => void = (): void => undefined;

describe("Add Tags modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddTagsModal).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    render(
      <AddTagsModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );

    expect(
      screen.queryByText("searchFindings.tabIndicators.tags.modalTitle")
    ).toBeInTheDocument();
  });

  it("should render input field and add button", (): void => {
    expect.hasAssertions();

    render(
      <AddTagsModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );

    expect(screen.queryByRole("textbox")).toBeInTheDocument();
    expect(screen.queryAllByRole("button")).toHaveLength(5);
  });

  it("should add and remove a input field", async (): Promise<void> => {
    expect.hasAssertions();

    const { container } = render(
      <AddTagsModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );

    expect(screen.queryAllByRole("textbox")).toHaveLength(1);
    expect(screen.queryAllByRole("button")).toHaveLength(5);
    expect(container.querySelector(".fa-trash-can")).not.toBeInTheDocument();

    await userEvent.click(screen.getAllByRole("button")[2]);
    await waitFor((): void => {
      expect(screen.queryAllByRole("textbox")).toHaveLength(2);
    });

    expect(screen.queryAllByRole("button")).toHaveLength(6);

    await userEvent.click(screen.getAllByRole("button")[1]);
    await waitFor((): void => {
      expect(screen.queryAllByRole("textbox")).toHaveLength(1);
    });
  });
});
