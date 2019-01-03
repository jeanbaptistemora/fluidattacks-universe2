import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import {
  compulsoryNotice as CompulsoryNotice
} from './index';
import { default as Modal } from "../../../../components/Modal/index";
import 'mocha';
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

Enzyme.configure({ adapter: new Adapter() });

describe('Compulsory notice modal', () => {
  it('should return a function', () => {
    expect(typeof(CompulsoryNotice)).to.equal('function');
  });

  it('should be rendered', () => {
    const wrapper = shallow(
      <CompulsoryNotice
        content=""
        id="testModal"
        open={true}
        rememberDecision={false}
        onAccept={(): void => undefined}
        onCheckRemember={(): void => undefined}
      />
    ),

    component = wrapper.find(Modal)
    expect(component).to.exist;
  });
});
