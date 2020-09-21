import { default as $ } from "jquery";

const setAnchors: (() => void) = (): void => {
  $(() => {
    let hTag: number;
    for (hTag = 1; hTag < 5; hTag += 1) {
    const tag: string = hTag.toString();
    const pageTitles: HTMLCollection = document.getElementsByTagName(`h${tag}`);

    for (const title of pageTitles) {
        let titleContent: string = (title as HTMLElement).innerText.toLowerCase();
        titleContent = titleContent.replace(/^[0-9.]*\s/, "");
        titleContent = titleContent.replace(/[¡!¿?,':\.]/g, "");
        titleContent = titleContent.replace(/\s+/g, "-");
        $(title)
            .prepend(`<a href="#${titleContent}"></a>`);
        $(title)
            .prepend(`<span id="${titleContent}"></span>`);
    }
    }
  });
};

setAnchors();

// Fix issues with anchors in Chrome
const fixAnchors: (() => void) = (): void => {
  $(() => {
    const isChrome: boolean = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
    // tslint:disable-next-line: strict-boolean-expressions
    if (window.location.hash && isChrome) {
        setTimeout(() => {
            const hash: string = window.location.hash;
            window.location.hash = "";
            window.location.hash = hash;
        },         300);
    }
  });
};

fixAnchors();
