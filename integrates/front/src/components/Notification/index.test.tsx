import { render, screen } from "@testing-library/react";
import React from "react";

import { Notification } from "components/Notification";

describe("Notification", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Notification).toStrictEqual("function");
  });

  it("should render a notification", (): void => {
    expect.hasAssertions();

    render(<Notification text={"text test"} title={"Title test"} />);

    expect(screen.queryByText("text test")).toBeInTheDocument();
    expect(screen.queryByText("Title test")).toBeInTheDocument();
  });
});
