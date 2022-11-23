import { render, screen } from "@testing-library/react";
import React from "react";

import { Text } from ".";

describe("Text", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Text).toBe("object");
  });

  it("should render a text", (): void => {
    expect.hasAssertions();

    render(<Text>{"Example Text"}</Text>);

    expect(screen.queryByText("Example Text")).toBeInTheDocument();
  });
});
