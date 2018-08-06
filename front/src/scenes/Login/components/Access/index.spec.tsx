import { shallow, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { expect } from 'chai';
import Access from './index';
import 'mocha';

configure({ adapter: new Adapter() });

describe('Login', () => {

  it('should return a function', () => {
    expect(typeof(Access)).to.equal('function');
  });

});