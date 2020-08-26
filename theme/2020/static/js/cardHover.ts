let accordions: HTMLCollection = document.getElementsByClassName("accordion");
let readmores: HTMLCollection = document.getElementsByClassName("readmore");

let count: number;
for (count = 0; count < accordions.length; count += 1) {
  accordions[count].addEventListener("click", (event: Event) => {
    (event.currentTarget as HTMLElement).classList.toggle("active");
    const panel: HTMLElement = (event.currentTarget as HTMLElement).nextElementSibling as HTMLElement;
    const arrow: HTMLElement = (panel.nextElementSibling as HTMLElement).children[1] as HTMLElement;

    arrow.classList.toggle("rotate-180");
    // tslint:disable-next-line: strict-boolean-expressions
    panel.style.maxHeight ?
    panel.style.maxHeight = ""
    : panel.style.maxHeight = `${panel.scrollHeight}px`;

    // tslint:disable-next-line: strict-boolean-expressions
    panel.style.minHeight ?
    panel.style.minHeight = ""
    : panel.style.minHeight = "360px";
  });
}

for (count = 0; count < readmores.length; count += 1) {
  readmores[count].addEventListener("click", (event: Event) => {
    (event.currentTarget as HTMLElement).classList.toggle("active");
    const panel: HTMLElement = (event.currentTarget as HTMLElement).previousElementSibling as HTMLElement;
    (panel.previousElementSibling as HTMLElement).click();
  });
}
