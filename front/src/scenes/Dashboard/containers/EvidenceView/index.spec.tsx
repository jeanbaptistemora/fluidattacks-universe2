import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { component as EvidenceView } from "./index";
import "mocha";
import React from "react";

configure({ adapter: new Adapter() });

describe('Evidence view', () => {

  it('should return a function', () => {
    expect(typeof (EvidenceView)).to.equal('function');
  });

  it('should render lightbox', () => {
    const wrapper = shallow(
      <EvidenceView
        canEdit={true}
        currentIndex={0}
        findingId="422286126"
        images={[
          {
            description: "Test evidence",
            url: "https://fluidattacks.com/test.png",
          }
        ]}
        isEditing={false}
        isImageOpen={true}
      />
    );

    expect(wrapper.find('ReactImageLightbox').length).to.equal(1);
  });
});
