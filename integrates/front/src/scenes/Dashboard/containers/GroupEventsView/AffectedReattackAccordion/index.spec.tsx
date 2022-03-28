import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
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

    const wrapper: ReactWrapper = mount(
      <Formik initialValues={{ affectedReattacks: [] }} onSubmit={jest.fn()}>
        <Form name={""}>
          <AffectedReattackAccordion findings={testFindings} />
        </Form>
      </Formik>
    );

    expect(wrapper).toHaveLength(1);
  });
});
