import * as React from 'react';
import { expect } from 'chai';
import { shallow, configure } from 'enzyme';
import { confirmDialog as ConfirmDialog } from './index';
import 'mocha';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('Confirm dialog', () => {

  it('should return a function', () => {
    expect(typeof (ConfirmDialog)).to.equal('function');
  });

  it('should render', () => {
    const wrapper = shallow(
      <ConfirmDialog
        open={true}
        title="Test"
        onProceed={(): void => undefined}
      />
    );
    expect(wrapper).to.have.length(1);
  });
});
