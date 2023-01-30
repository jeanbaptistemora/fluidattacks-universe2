import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React, { useCallback } from "react";

import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { IConfirmFn } from "components/ConfirmDialog";

describe("ConfirmDialog", (): void => {
  const btnCancel = "components.modal.cancel";
  const confirmCallback: jest.Mock = jest.fn();
  const cancelCallback: jest.Mock = jest.fn();
  const TestComponent: React.FC = (): JSX.Element => {
    const handleClick = useCallback(
      (confirm: IConfirmFn): (() => void) =>
        (): void => {
          confirm(confirmCallback, cancelCallback);
        },
      []
    );

    return (
      <ConfirmDialog title={"Title test"}>
        {(confirm): React.ReactNode => {
          return (
            <Button onClick={handleClick(confirm)} variant={"primary"}>
              {"Test"}
            </Button>
          );
        }}
      </ConfirmDialog>
    );
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ConfirmDialog).toBe("function");
  });

  it("should handle cancel", async (): Promise<void> => {
    expect.hasAssertions();

    render(<TestComponent />);

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(screen.queryByText("Title test")).not.toBeInTheDocument();

    await userEvent.click(screen.getByText("Test"));
    await waitFor((): void => {
      expect(screen.queryByText("Title test")).toBeInTheDocument();
    });

    expect(screen.queryByText(btnCancel)).toBeInTheDocument();

    await userEvent.click(screen.getByText(btnCancel));
    await waitFor((): void => {
      expect(cancelCallback).toHaveBeenCalledTimes(1);
    });

    expect(screen.queryByText("Title test")).not.toBeInTheDocument();
    expect(confirmCallback).toHaveBeenCalledTimes(0);
  });
});
