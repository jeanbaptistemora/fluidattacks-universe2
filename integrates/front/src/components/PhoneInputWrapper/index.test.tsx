/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen } from "@testing-library/react";
import React from "react";

import { PhoneInputWrapper } from ".";

describe("PhoneInputWrapper", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof PhoneInputWrapper).toBe("function");
  });

  it("should render phone input", (): void => {
    expect.hasAssertions();

    render(<PhoneInputWrapper />);

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(screen.queryByRole("textbox")).toBeInTheDocument();
  });
});
