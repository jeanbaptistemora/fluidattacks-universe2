import { useEffect, useState } from "react";

const useCarrousel = (
  delay: number,
  numberOfCycles: number
): { cycle: number; progress: number } => {
  const progressLimit = 100;
  const [cycle, setCycle] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect((): void => {
    const changeCycle = (): void => {
      setCycle((currentCycle): number =>
        currentCycle === numberOfCycles - 1 ? 0 : currentCycle + 1
      );
    };

    if (progress === progressLimit) {
      setProgress(0);
      changeCycle();
    }
  }, [progress, numberOfCycles]);

  useEffect((): (() => void) => {
    const timer = setInterval((): void => {
      setProgress((currentProgress): number =>
        currentProgress === progressLimit ? 0 : currentProgress + 1
      );
    }, delay);

    return (): void => {
      clearInterval(timer);
    };
  }, [delay]);

  return { cycle, progress };
};

const usePagination = (
  itemsToShow: number,
  listOfItems: (JSX.Element | undefined)[]
): {
  currentPage: number;
  endOffset: number;
  handlePageClick: (prop: { selected: number }) => void;
  newOffset: number;
  pageCount: number;
  resetPagination: () => void;
} => {
  const pageCount = Math.ceil(listOfItems.length / itemsToShow);
  const [newOffset, setNewOffset] = useState(0);
  const [endOffset, setEndOffset] = useState(itemsToShow);
  const [currentPage, setCurrentPage] = useState(0);

  const resetPagination = (): void => {
    setNewOffset(0);
    setEndOffset(itemsToShow);
    setCurrentPage(0);
  };

  const handlePageClick = (prop: { selected: number }): void => {
    const { selected } = prop;
    setCurrentPage(selected);
    setNewOffset((selected * itemsToShow) % listOfItems.length);
    setEndOffset(((selected * itemsToShow) % listOfItems.length) + itemsToShow);
  };

  return {
    currentPage,
    endOffset,
    handlePageClick,
    newOffset,
    pageCount,
    resetPagination,
  };
};

export { useCarrousel, usePagination };
