import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { RejectDraftModal } from "scenes/Dashboard/components/RejectDraftModal";

const functionMock: () => void = (): void => undefined;

describe("Reject draft modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof RejectDraftModal).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    render(
      <RejectDraftModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );

    expect(screen.queryByText("group.drafts.reject.title")).toBeInTheDocument();
    expect(
      screen.queryByRole("combobox", { name: "reason" })
    ).toBeInTheDocument();
    expect(screen.getAllByRole("option")).toHaveLength(8);
  });

  it("should render and validate other reason", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <RejectDraftModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );

    expect(screen.queryByLabelText("other")).not.toBeInTheDocument();
    expect(screen.queryByText("group.drafts.reject.title")).toBeInTheDocument();

    userEvent.selectOptions(screen.getByLabelText("reason"), "OTHER");

    await waitFor((): void => {
      expect(screen.queryByLabelText("other")).toBeInTheDocument();
    });

    expect(screen.queryByText("validations.required")).not.toBeInTheDocument();

    userEvent.click(screen.getByLabelText("other"));
    fireEvent.blur(screen.getByLabelText("other"));

    await waitFor((): void => {
      expect(screen.queryByText("validations.required")).toBeInTheDocument();
    });
  });
});
