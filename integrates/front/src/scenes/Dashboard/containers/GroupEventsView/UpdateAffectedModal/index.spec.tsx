import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { Form, Formik } from "formik";
import React from "react";

import { UpdateAffectedModal } from ".";
import type { IEventsDataset } from "..";
import type { IFinding } from "../AffectedReattackAccordion/types";

describe("Update Affected Modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof UpdateAffectedModal).toStrictEqual("function");
  });

  it("should render modal component", (): void => {
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

    const testEventsInfo: IEventsDataset = {
      group: {
        events: [
          {
            accessibility: "Repository",
            actionAfterBlocking: "NONE",
            actionBeforeBlocking: "NONE",
            affectedComponents: "",
            closingDate: "-",
            detail: "Test description",
            eventDate: "2018-10-17 00:00:00",
            eventStatus: "CREATED",
            eventType: "AUTHORIZATION_SPECIAL_ATTACK",
            groupName: "unittesting",
            id: "463457733",
          },
        ],
      },
    };

    const wrapper: ReactWrapper = mount(
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

    expect(wrapper).toHaveLength(1);
  });
});
