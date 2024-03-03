from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect

import requests

from django.core.paginator import Paginator

# Create your views here.

my_objects = []

def home(request):
    my_objects.clear()
    
    api_key = '28d4159b3cb94bd2b82235f96a788189'

    try:
        
        if request.method == 'POST':
            category = request.POST['category']
        else:
            category = 'business'


        base_url = f'https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={api_key}'

        print(base_url)

        response = requests.get(base_url)
        data = response.json()
        # print(data)

        id = 0
        if 'articles' in data:
            object = data['articles']
            for i in object:
                i['id'] = id
                id += 1
                # print(i['id'])


            # print(object)
            for x in object:
                id = x['id']
                title = x['title']
                author = x['author']
                image = x['urlToImage']
                desc = x['description']
                date = x['publishedAt']
                url  = x['url']
                
                my_objects.append({'id':id,'title':title, 'author':author, 'image':image, 'desc':desc, 'date':date, 'url':url})


            paginator = Paginator(object, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

        return render(request, 'base/home.html',context={'page_obj':page_obj,'category':category})

    except Exception as e:
        print(e)
        return render(request, 'base/home.html')



def about(request):
    return render(request, 'base/about.html')

def contact(request):
    return render(request, 'base/contact.html')


def post(request,id):
    try:
        # print(my_objects[id])
        object = my_objects[id]           
        return render(request, 'base/post.html', context={'object':object})
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/')

