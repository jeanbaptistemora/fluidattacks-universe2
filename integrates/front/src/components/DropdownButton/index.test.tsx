import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { MenuItem } from "components/DropdownButton";

const list: string[] = [];

describe("DropdownButton", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof MenuItem).toStrictEqual("function");
  });

  it("should render a button", (): void => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    render(
      <MenuItem
        eventKey={"test"}
        itemContent={
          <React.Fragment>
            {list}
            {list}
          </React.Fragment>
        }
        onClick={clickCallback}
      />
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
  });

  it("should be clickable", async (): Promise<void> => {
    expect.hasAssertions();

    const clickCallback: jest.Mock = jest.fn();
    render(
      <MenuItem
        eventKey={"test"}
        itemContent={
          <React.Fragment>
            {list}
            {list}
          </React.Fragment>
        }
        onClick={clickCallback}
      />
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();

    userEvent.click(screen.getByRole("button"));
    await waitFor((): void => {
      expect(clickCallback).toHaveBeenCalledTimes(1);
    });
  });
});
