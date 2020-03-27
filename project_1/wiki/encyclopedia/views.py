from django.shortcuts import render

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
        "entry": util.get_entry(title)
    })
