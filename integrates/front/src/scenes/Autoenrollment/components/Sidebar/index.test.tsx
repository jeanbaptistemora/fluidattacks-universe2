/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { Sidebar } from "scenes/Autoenrollment/components/Sidebar";

describe("Sidebar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Sidebar).toBe("function");
  });

  it("should render a sidebar", (): void => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/home"]}>
        <Sidebar />
      </MemoryRouter>
    );

    expect(screen.queryByRole("link")).toBeInTheDocument();
    expect(screen.getByRole("link")).toHaveAttribute("href", "/home");
  });
});
