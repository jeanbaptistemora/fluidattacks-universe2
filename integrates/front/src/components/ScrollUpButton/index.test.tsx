/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { ScrollUpButton } from "components/ScrollUpButton";

describe("ScrollUpButton", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ScrollUpButton).toBe("function");
  });
});
