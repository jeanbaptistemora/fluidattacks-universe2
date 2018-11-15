import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import {
  component as CompulsoryNotice
} from './index';
import { default as Modal } from "../../../../components/Modal/index";
import 'mocha';
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { Button, Checkbox } from "react-bootstrap";

Enzyme.configure({ adapter: new Adapter() });

describe('Compulsory notice modal', () => {
  it('should return a function', () => {
    expect(typeof(CompulsoryNotice)).to.equal('function');
  });

  it('should be rendered', () => {
    const wrapper = shallow(
      <CompulsoryNotice
        id="testModal"
        open={true}
        rememberDecision={false}
        loadDashboard={(): void => {}}
      />
    ),

    component = wrapper.find(Modal)
    expect(component).to.exist;
  });
});
