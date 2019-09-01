#food_list view as a function
from django.shortcuts import render,get_object_or_404
from .models import Food, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailFoodForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings

def food_list(request):
    object_list = Food.objects.all()    
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        foods = paginator.page(page)
    except PageNotAnInteger: # If page is not an integer deliver the first page
        foods = paginator.page(1)
    except EmptyPage: # If page is out of range deliver last page of results
        foods = paginator.page(paginator.num_pages)
    return render(
    request,
    'foodblog/food/list.html',
    {'page': page,
    'foods': foods}
    )

#--------------------------------------------------------------------------------


#food_detail view as a function

def food_detail(request, year, month, day, food):
    food = get_object_or_404(
    Food,
    slug=food,
    status='published',
    publish__year=year,
    publish__month=month,
    publish__day=day
    )
    # List of active comments for this post
    comments = food.comments.filter(active=True)
    commented=False
    if request.method == 'POST':
    # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
    # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
    # Assign the current post to the comment
            new_comment.food = food
    # Save the comment to the database
            new_comment.save()
            commented=True
    else:
        comment_form = CommentForm()
    return render(
    request,
    'foodblog/food/detail.html',
    {'food': food,
    'commented':commented,
    'comments': comments,
    'comment_form': comment_form}
    )

#------------------------------------------------------------------------------


#food_share view as a function

def food_share(request, food_id):
# Retrieve food by id
    food = get_object_or_404(Food, id=food_id, status='published')
    sent = False
    if request.method == 'POST':
    # Form was submitted
        form = EmailFoodForm(request.POST)
        if form.is_valid():
    # Form fields passed validation
            cd = form.cleaned_data
            food_url = request.build_absolute_uri(food.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'. format(cd['name'],
            cd['email'],
            food.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'. format(food.title,
            food_url,
            cd['name'],
            cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailFoodForm()
    return render(request,
        'foodblog/food/share.html',
        {'food': food,
        'form': form,
        'sent': sent}
        )
