import React from "react";
import Lightbox from "react-image-lightbox";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Disabling this two rules is necessary for
 * allowing the import of default styles that react-image-lightbox needs
 * to display properly even if some of them are overridden later
 */
import "react-image-lightbox/style.css";

interface IEvidenceLightboxProps {
  evidenceImages: Array<{ description?: string; url: string }>;
  index: number;
  onChange(index: number): void;
}

const evidenceLightbox: React.FC<IEvidenceLightboxProps> = (props: IEvidenceLightboxProps): JSX.Element => {
  const baseUrl: string = window.location.href.replace("dashboard#!/", "");

  const nextIndex: number = (props.index + 1) % props.evidenceImages.length;
  const moveNext: (() => void) = (): void => { props.onChange(nextIndex); };

  const previousIndex: number = (props.index + props.evidenceImages.length - 1) % props.evidenceImages.length;
  const movePrevious: (() => void) = (): void => { props.onChange(previousIndex); };

  const adjustZoom: (() => void) = (): void => {
    /**
     * As a workaround to a bug in react-image-lightbox,
     * we need trigger the resize event for it to properly calculate the image scale
     */
    setTimeout((): void => { window.dispatchEvent(new Event("resize")); }, 50);
    document.body.style.overflow = "hidden";
  };

  const closeImage: (() => void) = (): void => {
    document.body.style.removeProperty("overflow");
    props.onChange(-1);
  };

  return props.index > -1 ? (
    <Lightbox
      mainSrc={`${baseUrl}/${props.evidenceImages[props.index].url}`}
      nextSrc={`${baseUrl}/${props.evidenceImages[nextIndex].url}`}
      prevSrc={`${baseUrl}/${props.evidenceImages[previousIndex].url}`}
      imagePadding={50}
      imageTitle={props.evidenceImages[props.index].description}
      onAfterOpen={adjustZoom}
      onCloseRequest={closeImage}
      onMoveNextRequest={moveNext}
      onMovePrevRequest={movePrevious}
      reactModalStyle={{ overlay: { zIndex: "1200" } }}
    />
  ) : <React.Fragment />;
};

export { evidenceLightbox as EvidenceLightbox };
