from django.views import View
from django.shortcuts import render, redirect
from django import forms
from Richmond_Library_App.models import User, Book, Collection

class AddBookToCollectionForm(forms.ModelForm):
    collection_name = forms.CharField(max_length=100)  # Add a field for the collection name

    class Meta:
        model = Collection
        fields = ['book', 'collection_name']  # Include the new field

class Profile(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("http://127.0.0.1:8000/")
        
        user = User.objects.get(username=request.user.username)
        
        # Create an instance of the form for adding a book to the collection
        add_book_form = AddBookToCollectionForm()
        
        # Fetch the user's book collection
        user_collection = Collection.objects.filter(user=user)
        
        return render(request, "profile.html", {"user": user, "add_book_form": add_book_form, "user_collection": user_collection})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('')
        
        user = User.objects.get(username=request.user.username)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email_address = request.POST.get('email_address')
        user.phone_number = request.POST.get('phone_number')
        user.save()

        if 'create_collection' in request.POST:
            # Handle the Create Collection action
            add_book_form = AddBookToCollectionForm(request.POST)
            if add_book_form.is_valid():
                collection_entry = add_book_form.save(commit=False)
                collection_entry.user = request.user
                collection_entry.save()
                add_book_form.save_m2m()

        elif 'view_collections' in request.POST:
            # Handle the View Collections action
            # You can redirect the user to a page to view their collections

        # Fetch the user's book collection
            user_collection = Collection.objects.filter(user=user)

        return render(request, "profile.html", {"user": user, "add_book_form": add_book_form, "user_collection": user_collection})
