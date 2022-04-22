import { render } from "@testing-library/react";
import React from "react";

import { FluidIcon } from "components/FluidIcon";

describe("FluidIcon", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FluidIcon).toBe("function");
  });

  it("should render an icon", (): void => {
    expect.hasAssertions();

    const { container } = render(
      <FluidIcon height={"20px"} icon={"authors"} width={"20px"} />
    );

    expect(container.querySelector(".container")).toBeInTheDocument();
  });
});
