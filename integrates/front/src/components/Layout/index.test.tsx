/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen } from "@testing-library/react";
import React from "react";

import { Col, Gap, Hr, Row } from ".";

describe("Col", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Col).toBe("object");
  });

  it("should render a col", (): void => {
    expect.hasAssertions();

    render(<Col>{"Col content"}</Col>);

    expect(screen.queryByText("Col content")).toBeInTheDocument();
  });
});

describe("Gap", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Gap).toBe("object");
  });

  it("should render a gap", (): void => {
    expect.hasAssertions();

    render(<Gap>{"Gap content"}</Gap>);

    expect(screen.queryByText("Gap content")).toBeInTheDocument();
  });
});

describe("Hr", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Hr).toBe("object");
  });
});

describe("Row", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Row).toBe("object");
  });

  it("should render a row", (): void => {
    expect.hasAssertions();

    render(<Row>{"Row content"}</Row>);

    expect(screen.queryByText("Row content")).toBeInTheDocument();
  });
});
