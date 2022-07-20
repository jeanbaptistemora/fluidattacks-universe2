import { render, screen } from "@testing-library/react";
import React from "react";

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
});
