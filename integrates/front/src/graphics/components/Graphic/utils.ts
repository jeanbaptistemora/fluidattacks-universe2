/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

export function hasIFrameError(
  iFrameRef: React.MutableRefObject<HTMLIFrameElement | null>
): boolean {
  return Boolean(
    iFrameRef.current?.contentDocument?.title.toLowerCase().includes("error")
  );
}
