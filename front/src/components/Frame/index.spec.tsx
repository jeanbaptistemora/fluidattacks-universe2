import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import Frame from './index';
import 'mocha'
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import style from "./index.css";
import { Col, Row } from "react-bootstrap";

Enzyme.configure({ adapter: new Adapter() });

describe('Frame', () => {

  it('should return a function', () => {
    expect(typeof(Frame)).to.equal('function');
  });

  it('should be render', () => {
    const wrapper = shallow((
      <Frame
				src="https://fluidattacks.com/forms/cierres"
				height={3000}
				id="id"
			/>
    ));
    const element = 
      <Row className={style.frame_container}>
        <Col xs={12} md={12} sm={12}>
          <iframe
            id="id"
            className={style.frame_content}
            width="100%"
            scrolling="no"
            frameBorder="0"
            height={3000}
            src="https://fluidattacks.com/forms/cierres"
          />
        </Col>
      </Row>;
    expect(wrapper.contains(element))
    .to.equal(true);
  });

});