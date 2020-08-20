from django.shortcuts import render
from django import forms
from . import util
from random import choice
from markdown2 import Markdown

class newSearchForm(forms.Form):#innherits from forms.Form
    search = forms.CharField(
        widget= forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}),
        label=''
    )

class newEntryForm(forms.Form):
    title = forms.CharField(
        widget = forms.TextInput(attrs={'placeholder':'What\'s the Title?'}),
        label=''
    )
    content = forms.CharField(
        widget = forms.Textarea(attrs={
            'placeholder':'Use Markdown formatting to style this entry\'s content.',
            'cols': '40',
            'rows': '5',
            'class': 'my-2'}),
        label=''
    )

class editEntryForm(forms.Form):
    title = forms.CharField(
        widget = forms.TextInput(attrs={'hidden': 'True'}),
        label=''
    )
    content = forms.CharField(
        widget = forms.Textarea(attrs={'cols': '40', 'rows': '5'}),
        label=''
    )

def markdowner(title):
    #This method converts MD into HTML
    return Markdown().convert(util.get_entry(title))

def index(request):
    return render(request, 'encyclopedia/index.html', {
        'entries': util.list_entries(),
        'header': 'All Pages',
        'form': newSearchForm()
    })

def wiki(request, title):
    return render(request, 'encyclopedia/entry.html', {
        'title': title,
        'entry': markdowner(title),
        'form': newSearchForm()
    })

def search(request):
    form = newSearchForm(request.POST)
    if form.is_valid():
            search = form.cleaned_data['search']
            entries_substring = []
            for entry in util.list_entries():
                if search.lower() in entry.lower():
                    if search.lower() != entry.lower():
                        entries_substring.append(entry)
                    else:
                        title = search
                        return render(request, 'encyclopedia/entry.html', {
                        'title': title,
                        'entry': util.get_entry(title),
                        'form': newSearchForm()
                        })
            if len(entries_substring):
                return render(request, 'encyclopedia/index.html', {
                'entries': entries_substring,
                'header': 'Matching Results',
                'form': newSearchForm()
                })
    #if there are no matching results for the search, then return All Pages List
    return render(request, 'encyclopedia/index.html', {
    'entries': util.list_entries(),
    'header': 'All Pages',
    'form': newSearchForm()
    })

def new_entry(request):
    if request.method == 'POST':
        form = newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    return render(request, 'encyclopedia/new_entry.html', {
                    'header': 'New Entry',
                    'form': newSearchForm(),
                    'new_entry_form': form,
                    'error_message': 'This Title already exist. Please try a different one'
                    })
            try:
                util.save_entry(title, content)
                return render(request, 'encyclopedia/entry.html', {
                    'title': title,
                    'entry': markdowner(title),
                    'form': newSearchForm()
                })
            except Exception as e:
            #If an error is encountered, return the form with its content and display an error message
                return render(request, 'encyclopedia/new_entry.html', {
            'header': 'New Entry',
            'form': newSearchForm(),
            'new_entry_form': form,
            'error_message': e
            })
    return render(request, 'encyclopedia/new_entry.html', {
        'header': 'New Entry',
        'form': newSearchForm(),
        'new_entry_form': newEntryForm(),
    })

def edit_entry(request, title):
    if request.method == 'POST':
        form = editEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            try:
                util.save_entry(title, content)
                return render(request, 'encyclopedia/entry.html', {
                    'title': title,
                    'entry': markdowner(title),
                    'form': newSearchForm()
                })
            except Exception as e:
                return render(request, 'encyclopedia/new_entry.html', {
            'header': 'New Entry',
            'form': newSearchForm(),
            'new_entry_form': form,
            'error_message': e
            })
    return render(request, 'encyclopedia/edit_entry.html', {
        'header': 'Edit Entry',
        'title': title,
        'editForm': editEntryForm( 
            initial = {'title': title, 'content': util.get_entry( title )},
            auto_id = 'False'
        ),
        'form': newSearchForm()
    })

def random(request):
    entry = choice(util.list_entries())
    return render(request, 'encyclopedia/entry.html', {
        'title': entry,
        'entry': markdowner(entry),
        'form': newSearchForm()
    })