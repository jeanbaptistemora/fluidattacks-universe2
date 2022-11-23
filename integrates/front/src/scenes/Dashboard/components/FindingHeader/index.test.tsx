import { render, screen } from "@testing-library/react";
import React from "react";

import { FindingHeader } from "scenes/Dashboard/components/FindingHeader";

describe("FindingHeader", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FindingHeader).toBe("function");
  });

  it("should render finding header", (): void => {
    expect.hasAssertions();

    render(
      <FindingHeader
        discoveryDate={""}
        estRemediationTime={"42.1"}
        openVulns={9}
        severity={2}
        status={"open"}
      />
    );

    expect(
      screen.queryByText("searchFindings.header.severity.label")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.header.estRemediationTime.label")
    ).toBeInTheDocument();
    expect(screen.queryByText("42.1")).toBeInTheDocument();
  });
});
