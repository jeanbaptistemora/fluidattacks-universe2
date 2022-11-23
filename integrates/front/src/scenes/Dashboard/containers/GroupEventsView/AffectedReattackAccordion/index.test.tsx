import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Form, Formik } from "formik";
import React from "react";

import type { IFinding } from "./types";
import { GET_FINDING_VULNS_TO_REATTACK } from "./VulnerabilitiesToReattackTable/queries";

import { AffectedReattackAccordion } from ".";

describe("Affected Reattack accordion", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AffectedReattackAccordion).toBe("function");
  });

  it("should render accordion component", async (): Promise<void> => {
    expect.hasAssertions();

    const testFindings: IFinding[] = [
      {
        id: "test-finding-id",
        title: "038. Business information leak",
        verified: false,
      },
    ];

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_VULNS_TO_REATTACK,
          variables: {
            findingId: "test-finding-id",
          },
        },
        result: {
          data: {
            finding: {
              id: "test-finding-id",
              vulnerabilitiesToReattackConnection: {
                edges: [
                  {
                    node: {
                      findingId: "test-finding-id",
                      id: "test-vuln-id",
                      specific: "9999",
                      where: "vulnerable entrance",
                    },
                  },
                ],
                pageInfo: {
                  endCursor: "cursor",
                  hasNextPage: false,
                },
              },
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mocks}>
        <Formik initialValues={{ affectedReattacks: [] }} onSubmit={jest.fn()}>
          <Form name={""}>
            <AffectedReattackAccordion findings={testFindings} />
          </Form>
        </Formik>
      </MockedProvider>
    );

    expect(
      screen.queryByText("038. Business information leak")
    ).toBeInTheDocument();

    await userEvent.click(screen.getByText("038. Business information leak"));

    expect(screen.queryByRole("table")).toBeInTheDocument();
  });
});
