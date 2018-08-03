import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import CompulsoryNotice from './index';
import 'mocha'
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { Button } from "react-bootstrap";
import style from "./index.css";

Enzyme.configure({ adapter: new Adapter() });

function testAlert(){
  alert("test");
}

describe('Compulsory notice modal', () => {
  it('should return a function', () => {
    expect(typeof(CompulsoryNotice)).to.equal('function');
  });

  it('should be rendered', () => {
    const wrapper = shallow(
      <CompulsoryNotice
        id="testModal"
        noticeTitle="Unit title"
        noticeText="Unit test"
        btnAcceptText="Accept"
        btnAcceptTooltip="Accept help text"
        rememberText="Remember?"
        rememberTooltip="Remember help text"
        onAccept={testAlert}
      />
    );

    expect(
      wrapper.contains(
        <div className={style.content} id='testModal'>
          <div className={style.header}>
            <h3 className={style.title}>Unit title</h3>
          </div>
          <div className={style.body}>
            <p>Unit test</p>
            <p title='Remember help text'>
              <input
                type="checkbox"
                id="remember_decision"
              />
              Remember?
            </p>
          </div>
          <div className={style.footer}>
            <Button
              bsStyle="primary"
              title="Accept help text"
              onClick={testAlert}
            >
              Accept
            </Button>
          </div>
        </div>
      )
    ).to.equal(true);
  });
});
