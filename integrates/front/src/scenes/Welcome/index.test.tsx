import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen } from "@testing-library/react";
import type { FetchMockStatic } from "fetch-mock";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { GET_STAKEHOLDER_ENROLLMENT } from "./queries";
import type { IGetStakeholderEnrollmentResult } from "./types";

import { Welcome } from ".";
import { GET_STAKEHOLDER_GROUPS } from "scenes/Autoenrollment/queries";
import type { IGetStakeholderGroupsResult } from "scenes/Autoenrollment/types";
import { EMAIL_DOMAINS_URL } from "scenes/Autoenrollment/utils";
import { getCache } from "utils/apollo";

describe("Welcome", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Welcome).toBe("function");
  });

  it("should render NoEnrolledUser component", async (): Promise<void> => {
    expect.hasAssertions();

    const enrollmentMock: MockedResponse<IGetStakeholderEnrollmentResult> = {
      request: {
        query: GET_STAKEHOLDER_ENROLLMENT,
      },
      result: {
        data: {
          me: {
            enrollment: { enrolled: false },
            userEmail: "jdoe@fluidattacks.com",
            userName: "John Doe",
          },
        },
      },
    };

    const groupsMock: MockedResponse<IGetStakeholderGroupsResult> = {
      request: {
        query: GET_STAKEHOLDER_GROUPS,
      },
      result: {
        data: {
          me: {
            organizations: [],
            trial: null,
            userEmail: "jdoe@fluidattacks.com",
          },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { status: 200, text: "" });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider cache={getCache()} mocks={[enrollmentMock, groupsMock]}>
          <Welcome />
        </MockedProvider>
      </MemoryRouter>
    );

    await expect(
      screen.findByText("login.noEnrolledUser.title")
    ).resolves.toBeInTheDocument();
  });

  it("should render dashboard", async (): Promise<void> => {
    expect.hasAssertions();

    const enrollmentMock: MockedResponse<IGetStakeholderEnrollmentResult> = {
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
        <MockedProvider cache={getCache()} mocks={[enrollmentMock]}>
          <Welcome />
        </MockedProvider>
      </MemoryRouter>
    );

    await expect(screen.findByRole("main")).resolves.toBeInTheDocument();
  });
});
