/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import { useMemo } from "react";

// eslint-disable-next-line fp/no-rest-parameters, @typescript-eslint/no-explicit-any
type Callable = (...args: any[]) => any;

// Delays and groups function calls
const useDebouncedCallback = <T extends Callable>(
  callback: T,
  wait: number
): _.DebouncedFunc<T> => {
  const debouncedCallback = useMemo(
    (): _.DebouncedFunc<typeof callback> => _.debounce(callback, wait),
    [callback, wait]
  );

  return debouncedCallback;
};

export { useDebouncedCallback };
