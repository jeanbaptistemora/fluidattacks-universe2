import { render, screen } from "@testing-library/react";
import React from "react";

import { ConcurrentSessionNotice } from "scenes/Dashboard/components/ConcurrentSessionNoticeModal";

describe("Concurrent session notice modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ConcurrentSessionNotice).toStrictEqual("function");
  });

  it("should be rendered", (): void => {
    expect.hasAssertions();

    render(<ConcurrentSessionNotice onClick={jest.fn()} open={true} />);

    expect(
      screen.queryByText("registration.concurrentSessionTitle")
    ).toBeInTheDocument();
    expect(screen.queryByText("registration.continueBtn")).toBeInTheDocument();
    expect(screen.queryByRole("button")).toBeInTheDocument();
  });
});
