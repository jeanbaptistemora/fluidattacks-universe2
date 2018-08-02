import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import CompulsoryNotice from './index';
import 'mocha'
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

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
        title="Unit title"
        text="Unit test"
        btnAcceptText="Accept"
        rememberText="Remember?"
        onClick={testAlert}
      />
    );

    expect(
      wrapper.contains(
        <div className="modal-colored-header" id='testModal'>
          <div className="modal-content">
            <div className="modal-header">
              <h3 className="modal-title">Unit title</h3>
            </div>
            <div className="modal-body">
              <p>Unit test</p>
              <p>
                <input type="checkbox" id="remember_decision"/>
                Remember?
              </p>
            </div>
            <div className="modal-footer">
              <button
                className="btn btn-primary"
                onClick={testAlert}
                type="button"
              >
                Accept
              </button>
            </div>
          </div>
        </div>
      )
    ).to.equal(true);
  });
});
