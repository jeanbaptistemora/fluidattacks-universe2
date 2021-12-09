import React, { useCallback } from "react";
import Lightbox from "react-image-lightbox";
import "react-image-lightbox/style.css";

interface IEvidenceLightboxProps {
  evidenceImages: { description?: string; url: string }[];
  index: number;
  onChange: (index: number) => void;
}

const EvidenceLightbox: React.FC<IEvidenceLightboxProps> = (
  props: IEvidenceLightboxProps
): JSX.Element => {
  const { index, evidenceImages } = props;
  const nextIndex: number = (index + 1) % evidenceImages.length;
  const moveNext: () => void = useCallback((): void => {
    props.onChange(nextIndex);
  }, [props, nextIndex]);
  const previousIndex: number =
    (index + evidenceImages.length - 1) % evidenceImages.length;
  const movePrevious: () => void = useCallback((): void => {
    props.onChange(previousIndex);
  }, [props, previousIndex]);

  const adjustZoom: () => void = useCallback((): void => {
    /**
     * As a workaround to a bug in react-image-lightbox,
     * we need trigger the resize event for it to properly calculate the image scale
     */
    const RESIZE_TIMEOUT: number = 50;
    setTimeout((): void => {
      window.dispatchEvent(new Event("resize"));
    }, RESIZE_TIMEOUT);
    document.body.style.overflow = "hidden"; // eslint-disable-line fp/no-mutation
  }, []);

  const closeImage: () => void = useCallback((): void => {
    document.body.style.removeProperty("overflow");
    props.onChange(-1);
  }, [props]);

  return index > -1 ? (
    <Lightbox
      imagePadding={50}
      imageTitle={evidenceImages[index].description}
      mainSrc={`${location.href}/${evidenceImages[index].url}`}
      nextSrc={`${location.href}/${evidenceImages[nextIndex].url}`}
      onAfterOpen={adjustZoom}
      onCloseRequest={closeImage}
      onMoveNextRequest={moveNext}
      onMovePrevRequest={movePrevious}
      prevSrc={`${location.href}/${evidenceImages[previousIndex].url}`}
      reactModalStyle={{ overlay: { zIndex: "1200" } }}
    />
  ) : (
    <React.StrictMode />
  );
};

export { EvidenceLightbox };
