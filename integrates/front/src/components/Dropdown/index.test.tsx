import { render, screen } from "@testing-library/react";
import React from "react";

import { Dropdown } from ".";

describe("Dropdown", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Dropdown).toBe("function");
  });

  it("should render a dropdown", (): void => {
    expect.hasAssertions();

    render(
      <Dropdown button={"Dropdown button"}>
        <p>{"Dropdown content"}</p>
      </Dropdown>
    );

    expect(screen.queryByText("Dropdown button")).toBeInTheDocument();
    expect(screen.queryByText("Dropdown content")).toBeInTheDocument();
  });
});
