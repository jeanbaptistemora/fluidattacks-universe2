import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { commentsView as CommentsView } from "./index";
import "mocha";
import React from "react";

configure({ adapter: new Adapter() });

describe('Finding comments view', () => {

  it('should return a function', () => {
    expect(typeof(CommentsView)).to.equal('function');
  });

  it('should render', () => {
    const wrapper = shallow(
      <CommentsView
        findingId="435326633"
        type="comment"
      />
    );

    expect(wrapper.find('[id="finding-comments"]')).to.have.lengthOf(1);
  });
});
