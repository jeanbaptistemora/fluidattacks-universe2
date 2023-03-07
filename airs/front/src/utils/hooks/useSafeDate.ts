import dayjs from "dayjs";
import { useEffect, useState } from "react";

const useBlogsDate = (date: string): string => {
  const [safeDate, setSafeDate] = useState("");

  useEffect((): void => {
    setSafeDate(dayjs(new Date(date)).format("MMMM D, YYYY"));
  }, [date]);

  return safeDate;
};

const useFilterDate = (nodeDate: string, date: string): boolean => {
  const [safeDate, setSafeDate] = useState(true);

  useEffect((): void => {
    if (date === "Last month") {
      setSafeDate(dayjs(nodeDate).isAfter(dayjs().subtract(1, "months")));
    } else if (date === "Last 6 months") {
      setSafeDate(dayjs(nodeDate).isAfter(dayjs().subtract(6, "months")));
    } else if (date === "Last year") {
      setSafeDate(dayjs(nodeDate).isAfter(dayjs().subtract(1, "year")));
    }
  }, [date, nodeDate]);

  return safeDate;
};

const useDateYear = (): number => {
  const [safeDate, setSafeDate] = useState(0);

  useEffect((): void => {
    setSafeDate(dayjs().year());
  }, []);

  return safeDate;
};

export { useBlogsDate, useDateYear, useFilterDate };
