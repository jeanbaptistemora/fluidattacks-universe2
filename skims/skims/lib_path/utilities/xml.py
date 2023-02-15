from bs4.element import (
    Tag,
)
import re


def lookahead_from_str(original_str: str) -> str:
    return "(?=.*" + original_str + ")"


def get_original_opening_tag(tag: Tag, content: str) -> str | None:
    tag_opening_re = re.compile(r"^<[^>]*>", re.DOTALL)
    split_opening_re = re.compile(r"\s+", re.DOTALL | re.M | re.I)

    if (
        (tag_raw_content := str(tag))
        and (tag_opening := tag_opening_re.match(tag_raw_content))
        and (tag_str := tag_opening.group())
    ):
        split_list = split_opening_re.split(tag_str)
        if len(split_list) < 2:
            return None

        match_pat = split_list[0].replace("<", r"<\s*")
        for attr_str in split_list[1:-1]:
            match_pat = match_pat + lookahead_from_str(attr_str)

        closure = split_list[-1].replace(">", "")
        match_pat = match_pat + lookahead_from_str(closure) + "[^>]*>"

        main_reg_ex = re.compile(match_pat, re.DOTALL | re.M | re.I)

        if (concidence := main_reg_ex.findall(content)) and (
            len(concidence) == 1
        ):
            return concidence[0]
    return None


def get_attribute_line(tag: Tag, content: str, dang_attr: str) -> int | None:
    current_line = tag.sourceline
    if original_tag := get_original_opening_tag(tag, content):
        attrs_by_line = original_tag.split("\n")
        for line in attrs_by_line:
            if dang_attr in line.lower():
                return current_line
            current_line += 1
    return None
