import { render } from "@testing-library/react";
import React from "react";

import { Loading } from ".";

describe("Loading", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Loading).toBe("object");
  });

  it("should render Loading", (): void => {
    expect.hasAssertions();

    const { container } = render(<Loading />);

    expect(container.querySelector(".sc-bdvvtL")).toBeInTheDocument();
  });
});
