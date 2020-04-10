import re

from random import randint
from django.shortcuts import redirect, render

from . import util


def index(request):

    entries = util.list_entries()
    entries_lowercase = [entry.lower() for entry in entries]

    matched_entries = []

    search_query = request.GET.get("q")

    if search_query:

        search_query_lowercase = search_query.lower()

        if search_query_lowercase in entries_lowercase:
            entry_index = entries_lowercase.index(search_query_lowercase)
            title = entries[entry_index]
            return entry(request, title)

        else:
            for lowercase_entry in entries_lowercase:
                if search_query_lowercase in lowercase_entry:
                    entry_index = entries_lowercase.index(lowercase_entry)
                    title = entries[entry_index]
                    matched_entries.append(title)
            return render(request, "encyclopedia/search.html", {
                "matched_entries": matched_entries
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown_to_html(util.get_entry(title))
    })


def random(request):

    entries = util.list_entries()

    random_index = randint(0, len(entries) - 1)
    random_title = entries[random_index]

    return redirect("entry", title=random_title)


def markdown_to_html(entry):
    print(type(entry))

    for line in entry:
        print(line)

        # Check if line is a heading
        # h1 = # heading
        # h2 = ## heading

        h1_heading_pattern = r"^#\s(.*)$"
        h1_heading_match = re.search(h1_heading_pattern, line)
        if h1_heading_match:
            content = re.sub(h1_heading_pattern, "<h1>\g<1></h1>", line)
            continue

        h2_heading_pattern = r"^##\s(.*)$"
        h2_heading_match = re.search(h2_heading_pattern, line)
        if h2_heading_match:
            content = re.sub(h2_heading_pattern, "<h2>\g<1></h2>", line)
            continue

        paragraph_pattern = r"^(.*)$"
        if not (h1_heading_match and h2_heading_match):
            content = re.sub(paragraph_pattern, "<p>\g<1></p>", line)

        # Check if line is a list
        # unordered list = * foo
        unordered_list_pattern = r"^\*\s(.*)$"
        content = re.sub(unordered_list_pattern, "<li>\g<1></li>", line)

        # Check if there's bold styling
        # bold = **foo**
        bold_pattern = r"\*{2}(.*)\*{2}"
        content = re.sub(bold_pattern, "<strong>\g<1></strong>", line)

        # Check if there's a link
        # link = [text](url)
        link_pattern = r"\[(.*)\]\((.*)\)"
        content = re.sub(link_pattern, '<a href="\g<2>">\g<1></a>', line)
