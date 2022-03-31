import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { Button } from "components/Button";

describe("Button", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Button).toStrictEqual("object");
  });

  it("should render a button", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    render(
      <Button onClick={clickCallback} variant={"primary"}>
        {"Test1"}
      </Button>
    );

    expect(screen.queryByRole("button", { name: "Test1" })).toBeInTheDocument();
  });

  it("should be clickable", async (): Promise<void> => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    render(
      <Button onClick={clickCallback} variant={"primary"}>
        {"Test2"}
      </Button>
    );

    expect(screen.queryByRole("button", { name: "Test2" })).toBeInTheDocument();

    userEvent.click(screen.getByRole("button", { name: "Test2" }));
    await waitFor((): void => {
      expect(clickCallback).toHaveBeenCalledTimes(1);
    });
  });
});
