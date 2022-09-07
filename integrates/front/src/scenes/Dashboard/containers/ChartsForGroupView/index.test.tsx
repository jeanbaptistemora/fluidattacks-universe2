/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { ChartsForGroupView } from "scenes/Dashboard/containers/ChartsForGroupView";

describe("ChartsForGroupView", (): void => {
  it("should return an function", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsForGroupView).toBe("function");
  });
});
