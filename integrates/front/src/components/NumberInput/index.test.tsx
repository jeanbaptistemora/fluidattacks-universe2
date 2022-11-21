/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { NumberInput } from ".";

describe("numberInput", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof NumberInput).toBe("function");
  });

  it("should render a spinbutton", (): void => {
    expect.hasAssertions();

    const onEnterCallback: jest.Mock = jest.fn();
    render(
      <NumberInput defaultValue={2} max={3} min={1} onEnter={onEnterCallback} />
    );

    expect(screen.queryByRole("spinbutton")).toBeInTheDocument();
    expect(screen.queryByRole("spinbutton")).toHaveValue(2);
  });

  it("should render a spinbutton with decimal places", (): void => {
    expect.hasAssertions();

    const onEnterCallback: jest.Mock = jest.fn();
    render(
      <NumberInput
        decimalPlaces={1}
        defaultValue={2.1}
        max={3}
        min={1}
        onEnter={onEnterCallback}
      />
    );

    expect(screen.queryByRole("spinbutton")).toHaveValue(2.1);
  });

  it("should call callback on enter with the current value", async (): Promise<void> => {
    expect.hasAssertions();

    const onEnterCallback: jest.Mock = jest.fn();
    render(
      <NumberInput defaultValue={2} max={3} min={1} onEnter={onEnterCallback} />
    );

    await userEvent.type(screen.getByRole("spinbutton"), "{enter}");

    expect(onEnterCallback).toHaveBeenCalledWith(2);
  });

  it("should call callback with value ended in .", async (): Promise<void> => {
    expect.hasAssertions();

    const onEnterCallback: jest.Mock = jest.fn();
    render(
      <NumberInput
        autoUpdate={true}
        decimalPlaces={1}
        defaultValue={2.0}
        max={3}
        min={1}
        onEnter={onEnterCallback}
      />
    );

    await userEvent.type(screen.getByRole("spinbutton"), "{backspace}");

    expect(onEnterCallback).toHaveBeenCalledWith(2.0);
  });
});
