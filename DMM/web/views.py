from django.shortcuts import render
from django.template import RequestContext
from web.models import UserForm, UserProfileForm

# Create your views here.
def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(
            request,
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def index(request):
    return render(request, 'index.html')

def posts(request):
    context = dict()
    context['post_content'] = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Et tamen tantis vectigalibus ad liberalitatem utens etiam sine hac Pyladea amicitia multorum te benivolentia praeclare tuebere et munies. Ita redarguitur ipse a sese, convincunturque scripta eius probitate ipsius ac moribus. Ratio ista, quam defendis, praecepta, quae didicisti, quae probas, funditus evertunt amicitiam, quamvis eam Epicurus, ut facit, in caelum efferat laudibus. Ut ad minora veniam, mathematici, poëtae, musici, medici denique ex hac tamquam omnium artificum officina profecti sunt. Scientiam pollicentur, quam non erat mirum sapientiae cupido patria esse cariorem.'
    return render(request, 'posts.html', context=context)
