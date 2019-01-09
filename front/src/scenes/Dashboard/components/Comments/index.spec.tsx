import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { component as Comments } from "./index";
import "mocha";
import React from "react";

configure({ adapter: new Adapter() });

describe('Comments Box', () => {

  it('should return a function', () => {
    expect(typeof (Comments)).to.equal('function');
  });

  it('should be render', () => {
    const wrapper = shallow(
      <Comments
        id="comments-test"
        onLoad={() => undefined}
        onPostComment={() => undefined}
      />
    );

    expect(
      wrapper.contains(
        <div id="comments-test" />
      )
    ).to.equal(true);
  });
});
