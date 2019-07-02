import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { component as RecordsView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Records view", () => {

  const dataset: object[] = [
    {
      Character: "Cobra Commander",
      Genre: "action",
      Release: "2013",
      Title: "G.I. Joe: Retaliation",
    },
    {
      Character: "Tony Stark",
      Genre: "action",
      Release: "2008",
      Title: "Iron Man",
    },
  ];

  it("should return a function", () => {
    expect(typeof (RecordsView))
      .toEqual("function");
  });

  it("should render an editable component", () => {
    const wrapper: ShallowWrapper = shallow(
      <RecordsView
        canEdit={true}
        findingId="422286126"
        dataset={dataset}
        isEditing={true}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a component", () => {
    const wrapper: ShallowWrapper = shallow(
      <RecordsView
        canEdit={false}
        findingId="422286126"
        dataset={dataset}
        isEditing={false}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
