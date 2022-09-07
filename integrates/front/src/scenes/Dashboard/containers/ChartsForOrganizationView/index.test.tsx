/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { ChartsForOrganizationView } from "scenes/Dashboard/containers/ChartsForOrganizationView";

describe("ChartsForOrganizationView", (): void => {
  it("should return an function", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsForOrganizationView).toBe("function");
  });
});
