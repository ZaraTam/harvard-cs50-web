from django.shortcuts import render

from . import util


def index(request):

    entries = util.list_entries()
    entries_lowercase = [entry.lower() for entry in entries]

    matched_entries = []

    search_query = request.GET.get("q", "").lower()

    if search_query and search_query in entries_lowercase:
        entry_index = entries_lowercase.index(search_query)
        title = entries[entry_index]
        return entry(request, title)

    else:
        for e in entries_lowercase:
            if search_query in e:
                entry_index = entries_lowercase.index(e)
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
