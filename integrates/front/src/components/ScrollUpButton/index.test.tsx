import { render } from "@testing-library/react";
import React from "react";

import { ScrollUpButton } from "components/ScrollUpButton";

describe("ScrollUpButton", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ScrollUpButton).toBe("function");
  });

  it("should render a scroll up button", (): void => {
    expect.hasAssertions();

    const { container } = render(<ScrollUpButton visibleAt={400} />);

    expect(container.querySelector("#scroll-up")).toBeInTheDocument();
  });
});
