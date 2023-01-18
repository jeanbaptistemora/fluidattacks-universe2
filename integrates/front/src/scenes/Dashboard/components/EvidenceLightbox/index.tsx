import {
  faAngleLeft,
  faAngleRight,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";
import ImageViewer from "react-simple-image-viewer";

interface IEvidenceLightboxProps {
  evidenceImages: { url: string }[];
  currentImage: number;
  onClose: (index: number, isOpen: boolean) => void;
}

const EvidenceLightbox: React.FC<IEvidenceLightboxProps> = (
  props: IEvidenceLightboxProps
): JSX.Element => {
  const { currentImage, evidenceImages, onClose } = props;
  const handleOnClose = useCallback((): void => {
    onClose(0, false);
  }, [onClose]);

  return currentImage >= 0 ? (
    <div aria-label={"ImageViewer"} role={"dialog"}>
      <ImageViewer
        backgroundStyle={{
          backgroundColor: "rgba(0,0,0,0.9)",
          zIndex: "100",
        }}
        closeComponent={<FontAwesomeIcon icon={faXmark} />}
        closeOnClickOutside={true}
        currentIndex={currentImage}
        disableScroll={true}
        leftArrowComponent={<FontAwesomeIcon icon={faAngleLeft} />}
        // eslint-disable-next-line react/jsx-no-bind
        onClose={handleOnClose}
        rightArrowComponent={<FontAwesomeIcon icon={faAngleRight} />}
        src={evidenceImages.map(
          (name: { url: string }): string => `${location.href}/${name.url}`
        )}
      />
    </div>
  ) : (
    <React.StrictMode />
  );
};

export { EvidenceLightbox };
