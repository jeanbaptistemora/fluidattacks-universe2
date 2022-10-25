/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { Button } from "components/Button";

describe("Button", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Button).toBe("function");
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

    await userEvent.click(screen.getByRole("button", { name: "Test2" }));
    await waitFor((): void => {
      expect(clickCallback).toHaveBeenCalledTimes(1);
    });
  });
});
