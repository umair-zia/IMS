from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout

# Create your views here.
# def signup_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             #log the user in
#             login(request, user)
#             return redirect('news:list')
#     else:
#         form = UserCreationForm()
#         form.fields['username'].widget.attrs.update({
#             'placeholder': ' Username....'
#         })
#         form.fields['password1'].widget.attrs.update({
#             'placeholder': ' Password....'
#         })
#         form.fields['password2'].widget.attrs.update({
#             'placeholder': ' Confirm Password....'
#         })
#
#     return render(request,'accounts/signup.html',{'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        form.fields['username'].widget.attrs.update({
            'placeholder': ' Username....',
            'class':'form-control'
        })
        form.fields['password'].widget.attrs.update({
            'placeholder': ' Password....',
            'class': 'form-control'
        })
        if form.is_valid():
            # log in user
            user = form.get_user()
            login(request,user)
            if'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('schedule:index')
    else:
        form = AuthenticationForm()
        form.fields['username'].widget.attrs.update({
            'placeholder': ' Username....',
            'class':'form-control'
        })
        form.fields['password'].widget.attrs.update({
            'placeholder': ' Password....',
            'class': 'form-control'
        })
    return render(request,'accounts/login.html',{'form':form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('schedule:index')