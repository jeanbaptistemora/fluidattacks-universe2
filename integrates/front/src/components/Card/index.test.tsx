/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen } from "@testing-library/react";
import React from "react";

import { Card } from ".";

describe("Card", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Card).toBe("function");
  });

  it("should render a card", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    render(
      <Card onClick={clickCallback} title={"Card title"}>
        {"Card body"}
      </Card>
    );

    expect(screen.queryByText("Card title")).toBeInTheDocument();
    expect(screen.queryByText("Card body")).toBeInTheDocument();
  });

  it("should render a card untitled and with img", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    const { queryByText } = render(
      <Card img={"Card img"} onClick={clickCallback} title={undefined}>
        {"Card body"}
      </Card>
    );

    expect(queryByText("Card img")).toBeInTheDocument();
    expect(queryByText("Card title")).not.toBeInTheDocument();
  });
});
