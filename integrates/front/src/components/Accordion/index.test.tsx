import { render, screen } from "@testing-library/react";
import React from "react";

import { Accordion } from ".";

describe("Accordion", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Accordion).toBe("function");
  });

  it("should render an accordion", (): void => {
    expect.hasAssertions();

    render(
      <Accordion header={"Accordion header"}>
        <p>{"Accordion content"}</p>
      </Accordion>
    );

    expect(screen.queryByText("Accordion header")).toBeInTheDocument();
    expect(screen.queryByText("Accordion content")).toBeInTheDocument();
  });
});
