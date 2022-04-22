import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { CompulsoryNotice } from "scenes/Dashboard/components/CompulsoryNoticeModal";

describe("Compulsory notice modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof CompulsoryNotice).toBe("function");
  });

  it("should be rendered", (): void => {
    expect.hasAssertions();

    render(<CompulsoryNotice onAccept={jest.fn()} open={true} />);

    expect(screen.getByText("legalNotice.title")).toBeInTheDocument();
  });

  it("should render checkbox", (): void => {
    expect.hasAssertions();

    render(<CompulsoryNotice onAccept={jest.fn()} open={true} />);

    expect(screen.getAllByRole("checkbox")).toHaveLength(1);
  });

  it("should submit", async (): Promise<void> => {
    expect.hasAssertions();

    const handleAccept: jest.Mock = jest.fn();
    render(<CompulsoryNotice onAccept={handleAccept} open={true} />);

    expect(
      screen.queryByText("legalNotice.acceptBtn.text")
    ).toBeInTheDocument();

    userEvent.click(screen.getByText("legalNotice.acceptBtn.text"));
    await waitFor((): void => {
      expect(handleAccept).toHaveBeenCalledTimes(1);
    });
    jest.clearAllMocks();
  });
});
