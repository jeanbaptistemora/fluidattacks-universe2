import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import CommentBox from "./index";
import "mocha";
import React from "react";

configure({ adapter: new Adapter() });

describe('Comment Box', () => {

  it('should return a function', () => {
    expect(typeof(CommentBox)).to.equal('function');
  });

  it('should be render', () => {
    const wrapper = shallow(
      <CommentBox
        type="comment"
        visible={true}
      />
    );

    expect(
      wrapper.contains(
        <div id="comment" className="tab-pane cont">
            <div id="comments-container"/>
        </div>
      )
    ).to.equal(true);
  });
});
