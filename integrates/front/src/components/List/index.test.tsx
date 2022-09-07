/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { List } from ".";

describe("List", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof List).toBe("function");
  });
});
