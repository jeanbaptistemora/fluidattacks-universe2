/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { ContentSwitcher } from ".";

describe("ContentSwitcher", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ContentSwitcher).toBe("function");
  });

  it("should render a content switcher", (): void => {
    expect.hasAssertions();

    render(
      <ContentSwitcher
        contents={[<p key={1}>{"Content1"}</p>, <p key={2}>{"Content2"}</p>]}
        initSelection={0}
        tabs={["Tab1", "Tab2"]}
      />
    );

    expect(screen.queryByRole("button", { name: "Tab1" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Tab2" })).toBeInTheDocument();

    expect(screen.queryByText("Content1")).toBeInTheDocument();

    userEvent.click(screen.getByRole("button", { name: "Tab2" }));

    expect(screen.queryByText("Content2")).toBeInTheDocument();

    userEvent.click(screen.getByRole("button", { name: "Tab1" }));

    expect(screen.queryByText("Content1")).toBeInTheDocument();
  });
});
