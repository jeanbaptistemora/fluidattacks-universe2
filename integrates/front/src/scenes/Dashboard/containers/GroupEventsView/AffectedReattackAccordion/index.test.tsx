import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Form, Formik } from "formik";
import React from "react";

import type { IFinding } from "./types";

import { AffectedReattackAccordion } from ".";

describe("Affected Reattack accordion", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AffectedReattackAccordion).toStrictEqual("function");
  });

  it("should render accordion component", (): void => {
    expect.hasAssertions();

    const testFindings: IFinding[] = [
      {
        id: "test-finding-id",
        title: "038. Business information leak",
        vulnerabilitiesToReattack: [
          {
            findingId: "test-finding-id",
            id: "test-vuln-id",
            specific: "9999",
            where: "vulnerable entrance",
          },
        ],
      },
    ];

    render(
      <Formik initialValues={{ affectedReattacks: [] }} onSubmit={jest.fn()}>
        <Form name={""}>
          <AffectedReattackAccordion findings={testFindings} />
        </Form>
      </Formik>
    );

    expect(
      screen.queryByText("038. Business information leak")
    ).toBeInTheDocument();

    userEvent.click(screen.getByText("038. Business information leak"));

    expect(screen.queryByRole("table")).toBeInTheDocument();
  });
});
