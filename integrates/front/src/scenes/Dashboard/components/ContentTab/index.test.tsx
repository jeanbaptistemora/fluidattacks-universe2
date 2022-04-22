import { render, screen } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { ContentTab } from "scenes/Dashboard/components/ContentTab";

describe("ContentTab", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ContentTab).toBe("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    render(
      <MemoryRouter>
        <ContentTab
          id={"test-id"}
          link={"test-link"}
          title={"Tab-Title"}
          tooltip={"Tab-Tooltip"}
        />
      </MemoryRouter>
    );

    expect(screen.queryByRole("link")).toBeInTheDocument();
  });
});
