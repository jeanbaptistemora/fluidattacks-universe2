import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import Preloader from './index';
import 'mocha'
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import style from "./index.css";

Enzyme.configure({ adapter: new Adapter() });

describe('Preloader', () => {

  it('should return a function', () => {
    expect(typeof(Preloader)).to.equal('function');
  });

  it('should be render', () => {
    const wrapper = shallow((
      <Preloader/>
    ));
    const element =
      <div id="full_loader" className={style.loader}>
        <img
          src="assets/img/loading.gif"
          width="100"
          height="100"
        />
      </div>
    expect(wrapper.contains(element))
    .to.equal(true);
  });

});
