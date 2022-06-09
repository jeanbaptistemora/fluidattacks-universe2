import { render, screen } from "@testing-library/react";
import React from "react";

import { ScrollContainer } from ".";

describe("ScrollContainer", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof ScrollContainer).toBe("object");
  });

  it("should render scroll container content", (): void => {
    expect.hasAssertions();

    render(
      <ScrollContainer>
        <p className={"hv-50"}>{"ScrollContainer content"}</p>
      </ScrollContainer>
    );

    expect(screen.queryByText("ScrollContainer content")).toBeInTheDocument();
  });
});
