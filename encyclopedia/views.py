from django.shortcuts import render, redirect
from . import util
import random


import markdown


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def random_page(request):
    entries = util.list_entries()
    rand_page = random.randint(0, len(entries) - 1)
    page = util.get_entry(entries[rand_page])
    return render(request, "encyclopedia/wiki.html", {
        "entries": markdown.markdown(page)
    })


def search(request):
    if request.method == "POST":
        data = request.POST.get('q')
        entries = util.get_entry(data)

        if entries == data and len(data) <= 2:
            list_entry = util.list_entries()
            # variable to hold list of titles with given substring
            new_entry = []
            # Iterate through the list to search for substrings
            for i in list_entry:
                if data.lower() in i.lower():
                    new_entry.append(i)
            return render(request, "encyclopedia/index.html", {
                "entries": new_entry})

        return redirect('wiki', data)


def wiki(request,name):
    """Holds the title for the edit function below"""
    global edit_title
    edit_title = name
    page = util.get_entry(name)
    # check for errors
    if page == name:
        return render(request, "encyclopedia/error.html", {"name": name})

    return render(request, "encyclopedia/wiki.html", {
        "entries": markdown.markdown(page)
        })


def new_page(request):
    return render(request, "encyclopedia/new_page.html")


def new_entry(request):
    """Make a new page entry."""
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        check = util.save_entry(title, content, "")
        if not check:
            return redirect('wiki', title)

    return render(request, "encyclopedia/error1.html", {"name": title})


def edit(request):
    if request.method == "POST":
        edit_content = util.get_entry(edit_title)
        return render(request, "encyclopedia/edit.html", {"edit": edit_content})


def save_edit(request):
    """Save the edited version of an encyclopedia entry."""
    if request.method == "POST":
        btn_name = "save"
        content = request.POST.get("content")
        check = util.save_entry(edit_title, content, btn_name)
        if not check:
            return redirect('wiki', edit_title)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })





