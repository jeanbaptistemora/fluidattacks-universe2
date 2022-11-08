/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { GroupVulnerabilitiesView } from ".";

describe("GroupVulnerabilitiesView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupVulnerabilitiesView).toBe("function");
  });
});
