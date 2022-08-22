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

  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should render", (): void => {
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

  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should render and validate other reason", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <RejectDraftModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    );

    // Check for the absence and then presence of the `other` field
    expect(screen.queryByText("group.drafts.reject.title")).toBeInTheDocument();
    expect(screen.queryByLabelText("other")).not.toBeInTheDocument();

    userEvent.selectOptions(screen.getByLabelText("reason"), "OTHER");
    await waitFor((): void => {
      expect(screen.queryByLabelText("other")).toBeInTheDocument();
    });

    // Validate required field
    expect(screen.queryByText("validations.required")).not.toBeInTheDocument();

    userEvent.click(screen.getByLabelText("other"));
    fireEvent.blur(screen.getByLabelText("other"));

    await waitFor((): void => {
      expect(screen.queryByText("validations.required")).toBeInTheDocument();
    });

    // Validate forbidden characters
    expect(
      screen.queryByText("Field cannot begin with the following character: '='")
    ).not.toBeInTheDocument();

    userEvent.type(screen.getByLabelText("other"), "=I'm trying to sql inject");
    fireEvent.blur(screen.getByLabelText("other"));
    await waitFor((): void => {
      expect(
        screen.queryByText(
          "Field cannot begin with the following character: '='"
        )
      ).toBeInTheDocument();
    });
  });
});
