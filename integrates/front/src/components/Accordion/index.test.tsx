import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { Accordion } from ".";

describe("Accordion", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Accordion).toBe("function");
  });

  it("should render an accordion", (): void => {
    expect.hasAssertions();

    render(
      <Accordion header={"Accordion header"}>
        <p>{"Accordion content"}</p>
      </Accordion>
    );

    expect(screen.queryByText("Accordion header")).toBeInTheDocument();
    expect(screen.queryByText("Accordion content")).toBeInTheDocument();
  });

  it("should render a collapsed Accordion and open it", async (): Promise<void> => {
    expect.hasAssertions();

    const { container } = render(
      <Accordion
        header={"Accordion header"}
        iconSide={"left"}
        initCollapsed={true}
      >
        <p>{"Accordion content"}</p>
      </Accordion>
    );

    expect(container.querySelector(".comp-container")).toHaveStyle(`height: 0`);

    await userEvent.click(screen.getByText("Accordion header"));
    await waitFor((): void => {
      expect(container.querySelector(".comp-container")).not.toHaveStyle(
        `height: 0`
      );
    });
  });
});
