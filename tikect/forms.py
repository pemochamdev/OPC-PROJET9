from django import forms

from .models import Ticket, Review

class TicketForm(forms.ModelForm):
    title = forms.CharField(
        max_length=128,
        widget=forms.TextInput()
    )
    description = forms.CharField(
        max_length=2048,
        widget=forms.Textarea()
    )

    image = forms.ImageField(required=True)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline','rating', 'description']
        widgets = {
            'rating':forms.Select(attrs={
                'class':'form-control'
            })
        }


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    

class FollowUsersForm(forms.Form):

    class Meta:
        fields = ['followed_id']

    def __init__(self, *args, choices, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['followed_id'] = forms.ChoiceField(
            label='Nom utilisateur',
            choices=choices
            )
        #self.fields['followed_id'].widget.attrs.update({'class': 'form-user__add'})
        self.fields['followed_id'].widget.attrs.update(size='40')




class DeleteTicketReviewForm(forms.Form):
    """
    on créé notre model de formulaire DeleteTicketReviewForm

    Args:
        forms (object): on hérite du model de formulaire de django
    """

    delete_ticket_or_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

