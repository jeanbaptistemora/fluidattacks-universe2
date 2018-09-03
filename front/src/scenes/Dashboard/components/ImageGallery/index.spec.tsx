import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import ImageGallery from './index';
import 'mocha';
import { Col } from "react-bootstrap";
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import ReactImageGallery, { ReactImageGalleryProps } from "react-image-gallery";

Enzyme.configure({ adapter: new Adapter() });

describe('Image Gallery', () => {

  it('should return a function', () => {
    expect(typeof(ImageGallery)).to.equal('function');
  });

  it('should render image gallery', () => {
    const data = [
      {
        original: "image.png",
        originalTitle: "This is a title"
      }
    ];

    const wrapper = shallow(
      <ImageGallery
        items={data}
      />
    );

  let component = wrapper.find(  <ImageGallery infinite={true} items={data} showBullets={false} showFullscreenButton={true} showIndex={true}
      showNav={true} showThumbnails={true} thumbnailPosition="bottom" autoPlay={false} lazyLoad={false} showPlayButton={true}
      disableThumbnailScroll={false} disableArrowKeys={false} disableSwipe={false}
      useBrowserFullscreen={true} preventDefaultTouchmoveEvent={false} flickThreshold={0.4} stopPropagation={false}
      indexSeparator=" / " startIndex={0} slideDuration={450} swipingTransitionDuration={0} slideInterval={3000} swipeThreshold={30}
      renderLeftNav={(onClick: React.MouseEventHandler<HTMLElement>, isDisabled: boolean) => React}
      renderRightNav={(onClick: React.MouseEventHandler<HTMLElement>, isDisabled: boolean) => React}
      renderPlayPauseButton={(onClick: React.MouseEventHandler<HTMLElement>, isDisabled: boolean) => React}
      renderFullscreenButton={(onClick: React.MouseEventHandler<HTMLElement>, isDisabled: boolean) => React} />)
  expect(component).to.exist;
  });
});
