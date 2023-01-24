import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { act } from "react-dom/test-utils";

import { Alert } from ".";

describe("Alert", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Alert).toBe("function");
  });

  it("should render an alert", (): void => {
    expect.hasAssertions();

    render(<Alert>{"Alert message"}</Alert>);

    expect(screen.queryByText("Alert message")).toBeInTheDocument();
  });

  it("should hide a alert after 4sec", (): void => {
    expect.hasAssertions();

    jest.useFakeTimers();
    const { container } = render(
      <Alert autoHide={true} time={4}>
        {"Alert message"}
      </Alert>
    );

    expect(container.querySelector(".hgVEBv")).toBeInTheDocument();

    act((): void => {
      jest.runAllTimers();
    });

    expect(container.querySelector(".hgVEBv")).not.toBeInTheDocument();

    jest.useRealTimers();
  });

  it("should render a closable alert and close it", async (): Promise<void> => {
    expect.hasAssertions();

    jest.setTimeout(1000);
    const user = userEvent.setup();
    const { container } = render(
      <Alert closable={true}>{"Alert message"}</Alert>
    );

    expect(container.querySelector(".hgVEBv")).toBeInTheDocument();
    expect(screen.queryByRole("button")).toBeInTheDocument();

    await user.click(screen.getByRole("button"));
    await waitFor((): void => {
      expect(container.querySelector(".hgVEBv")).not.toBeInTheDocument();
    });
  });
});
