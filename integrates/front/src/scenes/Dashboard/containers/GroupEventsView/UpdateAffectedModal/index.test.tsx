import { render, screen } from "@testing-library/react";
import { Form, Formik } from "formik";
import React from "react";

import { UpdateAffectedModal } from ".";
import type { IFinding } from "../AffectedReattackAccordion/types";
import type { IEventsDataset } from "../types";

describe("update Affected Modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof UpdateAffectedModal).toBe("function");
  });

  it("should render modal component", (): void => {
    expect.hasAssertions();

    const testFindings: IFinding[] = [
      {
        id: "test-finding-id",
        title: "038. Business information leak",
        verified: false,
      },
    ];

    const testEventsInfo: IEventsDataset = {
      group: {
        events: [
          {
            closingDate: "-",
            detail: "Test description",
            eventDate: "2018-10-17 00:00:00",
            eventStatus: "CREATED",
            eventType: "DATA_UPDATE_REQUIRED",
            groupName: "unittesting",
            id: "463457733",
            root: null,
          },
        ],
      },
    };

    render(
      <Formik
        initialValues={{ affectedReattacks: [], eventId: "" }}
        onSubmit={jest.fn()}
      >
        <Form name={""}>
          <UpdateAffectedModal
            eventsInfo={testEventsInfo}
            findings={testFindings}
            onClose={jest.fn()}
            onSubmit={jest.fn()}
          />
        </Form>
      </Formik>
    );

    expect(
      screen.queryByText("group.events.form.affectedReattacks.title")
    ).toBeInTheDocument();
  });
});
