function setReportType(icon: SVGElement): string {
  if (
    (icon.attributes.getNamedItem("data-icon")?.value as string).includes("pdf")
  ) {
    return "PDF";
  }

  return (icon.attributes.getNamedItem("data-icon")?.value as string).includes(
    "excel"
  )
    ? "XLS"
    : "DATA";
}

export { setReportType };
