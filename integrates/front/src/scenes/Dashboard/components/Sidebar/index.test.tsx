import { render, screen } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { Sidebar } from "scenes/Dashboard/components/Sidebar";

describe("Sidebar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Sidebar).toBe("function");
  });

  it("should render a sidebar", (): void => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/home"]}>
        <Sidebar />
      </MemoryRouter>
    );

    expect(screen.queryByRole("link")).toBeInTheDocument();
    expect(screen.getByRole("link")).toHaveAttribute("href", "/home");
  });
});
