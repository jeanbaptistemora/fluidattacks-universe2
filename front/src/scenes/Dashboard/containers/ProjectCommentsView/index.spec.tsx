import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { projectCommentsView as CommentsView } from "./index";
import "mocha";
import React from "react";

configure({ adapter: new Adapter() });

describe('Project comments view', () => {

  it('should return a function', () => {
    expect(typeof(CommentsView)).to.equal('function');
  });

  it('should render', () => {
    const wrapper = shallow(
      <CommentsView
        projectName="unittesting"
      />
    );

    expect(wrapper.find('[id="project-comments"]')).to.have.lengthOf(1);
  });
});
