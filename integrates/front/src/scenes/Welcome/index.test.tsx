/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { GET_STAKEHOLDER_ENROLLMENT } from "./queries";
import type { IGetStakeholderEnrollmentResult } from "./types";

import { Welcome } from ".";

describe("Welcome", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Welcome).toBe("function");
  });

  it("should render dashboard", async (): Promise<void> => {
    expect.hasAssertions();

    const queryMock: MockedResponse<IGetStakeholderEnrollmentResult> = {
      request: {
        query: GET_STAKEHOLDER_ENROLLMENT,
      },
      result: {
        data: {
          me: {
            enrollment: { enrolled: true },
            userEmail: "jdoe@fluidattacks.com",
            userName: "John Doe",
          },
        },
      },
    };

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider addTypename={false} mocks={[queryMock]}>
          <Welcome />
        </MockedProvider>
      </MemoryRouter>
    );

    await expect(screen.findByRole("main")).resolves.toBeInTheDocument();
  });

  it("should render not elegible", async (): Promise<void> => {
    expect.hasAssertions();

    const queryMock: MockedResponse<IGetStakeholderEnrollmentResult> = {
      request: {
        query: GET_STAKEHOLDER_ENROLLMENT,
      },
      result: {
        data: {
          me: {
            enrollment: { enrolled: true },
            userEmail: "jdoe@fluidattacks.com",
            userName: "John Doe",
          },
        },
      },
    };
    sessionStorage.setItem("trial", "true");

    render(
      <MockedProvider addTypename={false} mocks={[queryMock]}>
        <Welcome />
      </MockedProvider>
    );

    await expect(
      screen.findByText("autoenrollment.notElegible")
    ).resolves.toBeInTheDocument();
  });
});
