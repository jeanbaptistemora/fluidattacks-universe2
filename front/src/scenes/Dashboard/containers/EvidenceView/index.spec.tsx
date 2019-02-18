import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { component as EvidenceView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Evidence view", () => {

  it("should return a function", () => {
    expect(typeof (EvidenceView)).to
      .equal("function");
  });

  it("should render lightbox", () => {
    const wrapper: ShallowWrapper = shallow(
      <EvidenceView
        canEdit={true}
        currentIndex={0}
        findingId="422286126"
        images={[{ description: "Test evidence", url: "https://fluidattacks.com/test.png" }]}
        isEditing={false}
        isImageOpen={true}
      />,
    );

    expect(wrapper.find("ReactImageLightbox").length).to
      .equal(1);
  });
});
