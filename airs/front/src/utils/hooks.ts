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

export { useCarrousel };
