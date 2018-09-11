import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import {
  compulsoryNoticeComponent,
  compulsoryNotice as CompulsoryNotice } from './index';
import Modal from "react-responsive-modal";
import 'mocha';
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { Button, Checkbox } from "react-bootstrap";

Enzyme.configure({ adapter: new Adapter() });

function onTestAccept(arg1: boolean){
  alert(`Accepted the terms. Remember preferences will be set to: ${arg1}`);
}

function onTestRememberCheck(arg1: boolean){
  alert(`Remember checkbox value: ${arg1}`);
}

describe('Compulsory notice modal', () => {
  it('should return a function', () => {
    expect(typeof(CompulsoryNotice)).to.equal('function');
  });

  it('should be rendered', () => {
    const wrapper = shallow(
      <CompulsoryNotice
        btnAcceptText="Accept"
        btnAcceptTooltip="Accept help text"
        id="testModal"
        noticeTitle="Unit test title"
        noticeText="Unit test modal content"
        open={true}
        rememberDecision={false}
        rememberText="Remember?"
        rememberTooltip="Remember help text"
        onAccept={(): void => { onTestAccept(false) }}
        onRememberCheck={() => { onTestRememberCheck(false) }}
      />
    ),

    // Get the component inside of ReduxWrapper
    component = wrapper.dive().find(compulsoryNoticeComponent)
    expect(component).to.exist;
  });
});
