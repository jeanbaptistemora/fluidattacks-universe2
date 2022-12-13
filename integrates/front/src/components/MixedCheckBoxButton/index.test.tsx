import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { MixedCheckBoxButton } from ".";

describe("MixedCheckBoxButton", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof MixedCheckBoxButton).toBe("function");
  });

  it("should render a MixedCheckBoxButton", (): void => {
    expect.hasAssertions();

    render(
      <MixedCheckBoxButton
        fontSize={"fs-checkbox"}
        id={"zeroRiskCheckBox"}
        noLabel={"REJECT"}
        yesLabel={"CONFIRM"}
      />
    );

    expect(screen.getByText("REJECT")).toBeInTheDocument();
    expect(screen.getByText("CONFIRM")).toBeInTheDocument();
  });

  it("should be a MixedCheckBoxButton clickable", async (): Promise<void> => {
    expect.hasAssertions();

    const handleOnApprove: jest.Mock = jest.fn();
    const user = userEvent.setup();
    render(
      <MixedCheckBoxButton
        fontSize={"fs-checkbox"}
        id={"zeroRiskCheckBox"}
        noLabel={"REJECT"}
        onApprove={handleOnApprove}
        yesLabel={"CONFIRM"}
      />
    );

    expect(screen.getByText("CONFIRM")).toBeInTheDocument();

    await user.click(screen.getByText("CONFIRM"));
    await waitFor((): void => {
      expect(handleOnApprove).toHaveBeenCalledTimes(1);
    });
  });
});
