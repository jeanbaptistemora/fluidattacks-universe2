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
        <p className={style.text}>
          <img
            src="assets/img/loading.gif"
            width="120"
            height="120"
          />
          <br/>
          Powered by <b>Fluid Attacks</b>
        </p>
      </div>
    expect(wrapper.contains(element))
    .to.equal(true);
  });

});
