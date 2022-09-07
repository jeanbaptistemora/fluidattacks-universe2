/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

function setReportType(icon: SVGElement): string {
  if (
    (icon.attributes.getNamedItem("data-icon")?.value as string).includes("pdf")
  ) {
    return "PDF";
  } else if (
    (icon.attributes.getNamedItem("data-icon")?.value as string).includes(
      "contract"
    )
  ) {
    return "CERT";
  }

  return (icon.attributes.getNamedItem("data-icon")?.value as string).includes(
    "excel"
  )
    ? "XLS"
    : "DATA";
}

export { setReportType };
