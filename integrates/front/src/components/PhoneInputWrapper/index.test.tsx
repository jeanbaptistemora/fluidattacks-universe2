import { render, screen } from "@testing-library/react";
import React from "react";

import { PhoneInputWrapper } from ".";

describe("PhoneInputWrapper", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof PhoneInputWrapper).toStrictEqual("function");
  });

  it("should render phone input", (): void => {
    expect.hasAssertions();

    render(<PhoneInputWrapper />);

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(screen.queryByRole("textbox")).toBeInTheDocument();
  });
});
