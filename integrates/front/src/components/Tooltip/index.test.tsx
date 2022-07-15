import { render, screen } from "@testing-library/react";
import React from "react";

import { Tooltip } from ".";

describe("Tooltip", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Tooltip).toBe("function");
  });

  it("should render a Tooltip", (): void => {
    expect.hasAssertions();

    render(<Tooltip id={"TooltipId"}>{"Tooltip content"}</Tooltip>);

    expect(screen.queryByText("Tooltip content")).toBeInTheDocument();
  });
});
