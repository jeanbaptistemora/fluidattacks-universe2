/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { Accordion } from ".";

describe("Accordion", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Accordion).toBe("function");
  });

  it("should render an accordion", (): void => {
    expect.hasAssertions();

    render(
      <Accordion header={"Accordion header"}>
        <p>{"Accordion content"}</p>
      </Accordion>
    );

    expect(screen.queryByText("Accordion header")).toBeInTheDocument();
    expect(screen.queryByText("Accordion content")).toBeInTheDocument();
  });

  it("should render a collapsed Accordion", async (): Promise<void> => {
    expect.hasAssertions();

    const { rerender } = render(
      <Accordion header={"Accordion header"}>
        <p>{"Accordion content"}</p>
      </Accordion>
    );

    expect(screen.queryByText("Accordion header")).toBeInTheDocument();

    await userEvent.click(screen.getByText("Accordion header"));
    await waitFor((): void => {
      rerender(
        <Accordion header={"Accordion header"} initCollapsed={true}>
          {""}
        </Accordion>
      );

      expect(screen.queryByText("Accordion content")).not.toBeInTheDocument();
    });
  });
});
