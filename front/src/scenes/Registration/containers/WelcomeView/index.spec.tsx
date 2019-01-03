import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import { component as WelcomeView } from './index';
import { component as CompulsoryNotice } from '../../components/CompulsoryNotice/index';
import 'mocha';
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

Enzyme.configure({ adapter: new Adapter() });

describe('Welcome view', () => {
  it('should return a function', () => {
    expect(typeof (WelcomeView)).to.equal('function');
  });

  it('should render', () => {
    const wrapper = shallow(
      <WelcomeView
        email={"unittesting@fluidattacks.com"}
        isAuthorized={false}
        isRememberEnabled={false}
        username={"Test"}
      />
    );

    expect(wrapper).to.have.length(1);
  });

  it('should render greetings message', () => {
    const wrapper = shallow(
      <WelcomeView
        email={"unittesting@fluidattacks.com"}
        isAuthorized={false}
        isRememberEnabled={false}
        username={"Test"}
      />
    );

    expect(wrapper.contains(<h1>registration.greeting Test!</h1>)).to.equal(true);
  });

  it('should render unauthorized message', () => {
    const wrapper = shallow(
      <WelcomeView
        email={"unittesting@fluidattacks.com"}
        isAuthorized={false}
        isRememberEnabled={false}
        username={"Test"}
      />
    );

    expect(wrapper.contains(<p>registration.unauthorized</p>)).to.equal(true);
  });

  it('should render legal notice', () => {
    const wrapper = shallow(
      <WelcomeView
        email={"unittesting@fluidattacks.com"}
        isAuthorized={true}
        isRememberEnabled={false}
        username={"Test"}
      />
    );

    expect(wrapper.find({ id: "legalNotice" }).length).to.equal(1);
  });
});
