import { render, screen } from "@testing-library/react";
import React from "react";

import { Container } from ".";

describe("Container", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Container).toBe("object");
  });

  it("should render a container", (): void => {
    expect.hasAssertions();

    render(
      <Container>
        <p>{"Container content"}</p>
      </Container>
    );

    expect(screen.queryByText("Container content")).toBeInTheDocument();
  });
});
