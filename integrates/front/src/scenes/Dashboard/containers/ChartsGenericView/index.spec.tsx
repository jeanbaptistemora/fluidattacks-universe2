import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import waitForExpect from "wait-for-expect";

import { SUBSCRIPTIONS_TO_ENTITY_REPORT } from "./queries";

import { Graphic } from "graphics/components/Graphic";
import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";

describe("ChartsGenericView", (): void => {
  const mocks: MockedResponse = {
    request: {
      query: SUBSCRIPTIONS_TO_ENTITY_REPORT,
    },
    result: {
      data: {
        me: {
          __typename: "Me",
          subscriptionsToEntityReport: [],
          userEmail: "",
        },
      },
    },
  };

  it("should return an function", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsGenericView).toStrictEqual("function");
  });

  it("should render a component and number of graphics of entity", async (): Promise<void> => {
    expect.hasAssertions();

    const groupGraphics: number = 28;
    const organizationAndPportfolioGraphics: number = 33;

    const wrapper: ReactWrapper = mount(
      <ChartsGenericView
        bgChange={false}
        entity={"organization"}
        reportMode={false}
        subject={"subject"}
      />,
      {
        wrappingComponent: MockedProvider,
        wrappingComponentProps: { addTypename: true, mocks: [mocks] },
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find(Graphic)).toHaveLength(
      organizationAndPportfolioGraphics
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.setProps({ entity: "group" });
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find(Graphic)).toHaveLength(groupGraphics);

        wrapper.setProps({ entity: "portfolio" });
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find(Graphic)).toHaveLength(
          organizationAndPportfolioGraphics
        );
      });
    });
  });
});
