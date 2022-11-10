/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render } from "@testing-library/react";
import React from "react";

import { ProgressBar, getPercentageToDisplay } from ".";

describe("ProgressBar", (): void => {
  it("should return functions", (): void => {
    expect.hasAssertions();
    expect(typeof ProgressBar).toBe("function");
    expect(typeof getPercentageToDisplay).toBe("function");
  });

  it("should render ProgressBar", (): void => {
    expect.hasAssertions();

    const { container } = render(<ProgressBar />);

    expect(container.querySelector(".sc-bczRLJ")).toBeInTheDocument();
  });

  it("should validate if statement", (): void => {
    expect.hasAssertions();
    expect(getPercentageToDisplay(101)).toBe(100);
  });
});
