import { useCallback, useEffect, useState } from "react";

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
  currentItems: (JSX.Element | undefined)[];
  handlePageClick: (prop: { selected: number }) => void;
  pageCount: number;
} => {
  const itemsPerPage = itemsToShow;
  const pageCount = Math.ceil(listOfItems.length / itemsPerPage);
  const [currentItems, setCurrentItems] = useState(
    listOfItems.slice(0, itemsPerPage)
  );

  const handlePageClick = useCallback(
    (prop: { selected: number }): void => {
      const { selected } = prop;
      const newOffset = (selected * itemsPerPage) % listOfItems.length;
      const endOffset = newOffset + itemsPerPage;
      setCurrentItems(listOfItems.slice(newOffset, endOffset));
    },
    [itemsPerPage, listOfItems]
  );

  return { currentItems, handlePageClick, pageCount };
};

export { useCarrousel, usePagination };
