/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render } from "@testing-library/react";
import React from "react";

import { Loading } from ".";

describe("Loading", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Loading).toBe("object");
  });

  it("should render Loading", (): void => {
    expect.hasAssertions();

    const { container } = render(<Loading />);

    expect(container.querySelector(".sc-bczRLJ")).toBeInTheDocument();
  });
});
