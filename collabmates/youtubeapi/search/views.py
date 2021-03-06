from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# Create your views here.        AIzaSyCc3ufj6dlc6EYkQ41pRgvpFWHAHT5wHdA
#mysql> ALTER TABLE collabmates.search_searchdetail CONVERT TO CHARACTER SET utf8mb4;
#virtualenv -p python3 .
from .models import SearchDetail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView

DEVELOPER_KEY = 'AIzaSyCc3ufj6dlc6EYkQ41pRgvpFWHAHT5wHdA'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

@csrf_exempt
def youtube_search(request,query,num=1):
 
    #checking if the method is GET Or POST
    if request.method=='GET':
        Q = SearchDetail.objects.all().filter(query = query).order_by('-datetime')
        #cheking if the query already exists i the database
        if not Q.exists():
            #if query is not in the database,throw an error
            json_res={"message":"Bad RequestUse POST method for new quries" }
            return JsonResponse(json_res)
        #else return a json file with required data
        json_res=[]
        page_request_var = 'page'
        page = request.GET.get(page_request_var)
        paginator = Paginator(Q, 10)  #paginating the queryset
        try:
            paginated_queryset = paginator.page(num)
        except PageNotAnInteger:
            paginated_queryset = paginator.page(1)
        except EmptyPage:
            paginated_queryset = paginator.page(paginator.num_pages)

        for item in paginated_queryset:
            json = {"title": item.title,"description":item.description,"thumbnail url":item.thumbnail,"published date":item.datetime}
            json_res.append(json)
        return JsonResponse(json_res,safe=False)

    #pcheck if the mrthod is POST
    if request.method=="POST":

        Q = SearchDetail.objects.all().filter(query = query).order_by('-datetime')
#check if query is in the database, if not , fetch the details from youtube api and stre it to the database
        if not Q.exists() : 
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
            search_response = youtube.search().list(q=query,part='id,snippet',maxResults=20,order = 'date', publishedAfter='2010-01-01T00:00:00Z').execute()
            #print(search_response)
            json_res = []
            success={"status": "True" ,"status code" : 200,"message":"OK"}
            json_res.append(success)
            for item in search_response['items']:
                datetime= item['snippet']['publishedAt']
                description = item['snippet']['description']
                title =item['snippet']['title']
                thumbnail = item['snippet']['thumbnails']['default']['url']
                #print(description)
                new = SearchDetail(title = title , description=description, thumbnail = thumbnail , datetime = datetime,query=query)
                new.save()

            return JsonResponse(json_res,safe=False)
#if query already exists , then just return the data associated with the query
        else:
            json_res = []
            success={"status": "True" ,"status code" : 200,"message":"Query already exists,Use GET method to get Data"}
            json_res.append(success)

            return JsonResponse(json_res,safe=False)
    

