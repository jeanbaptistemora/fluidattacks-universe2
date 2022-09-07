/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { ProgressIndicator } from ".";

describe("ProgressIndicator", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof ProgressIndicator).toBe("object");
  });
});
