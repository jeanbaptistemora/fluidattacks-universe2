/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Loading } from ".";

describe("Loading", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Loading).toBe("object");
  });
});
