/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen } from "@testing-library/react";
import React from "react";

import { InfoDropdown } from ".";

describe("InfoDropdown", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof InfoDropdown).toBe("function");
  });

  it("should display the content", (): void => {
    expect.hasAssertions();

    render(
      <InfoDropdown>
        <p>{"InfoDropdown content"}</p>
      </InfoDropdown>
    );

    expect(screen.queryByText("InfoDropdown content")).toBeInTheDocument();
  });
});
