from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from django.http import HttpResponse ,JsonResponse,HttpResponseRedirect
from django.template import loader
from .models import *
import json
from django.urls import reverse

# Create your views here.
def Main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def get_all_person(request):
    latest_intern=interns.objects.order_by("id")
    template = loader.get_template("get_all_person.html")
    context = {
        "latest_intern": latest_intern,
    }
    return HttpResponse(template.render(context, request))

def intern_details(request,id):
  intern = interns.objects.get(id=id)
  template = loader.get_template('intern_details.html')
  context = {
      'intern':intern
  }
  return HttpResponse(template.render(context, request))


def Get_Method(request):
    if request.method == 'GET':
        # Fetching all intern objects from the database (you can adjust this as per your requirements)
        interns = interns.objects.all()
        response_data = []
        for intern in interns:
            response_data.append({
                'id': intern.id,
                'name': intern.name,
                'email': intern.email,
                'age': intern.age,
                'test': intern.test,
            })
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
  
def delete_intern(request,id):
  intern = interns.objects.get(id=id)
  template = loader.get_template('delete.html')
  context = {
      'intern':intern
  }
  return HttpResponse(template.render(context, request))
  
def delete(request, id):
  if request.method == 'DELETE':
      item = get_object_or_404(interns, id=id)
      item.delete()
      return JsonResponse({'message': 'Item deleted successfully!'}, status=200)
  else:
      return JsonResponse({'message': 'Invalid method'}, status=405)


def update(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        intern = get_object_or_404(interns, id=id)
        intern.name = data.get("name", intern.name)
        intern.email = data.get("email", intern.email)
        intern.age = data.get("age", intern.age)
        intern.salary = data.get("salary", intern.salary)
        intern.save()
        return JsonResponse({'message': 'intern updated successfully!'}, status=200)
    return JsonResponse({'error': 'Invalid method. Use PUT.'}, status=405)

def update_intern(request,id):
  intern = interns.objects.get(id=id)
  template = loader.get_template('update.html')
  context = {
      'intern':intern
  }
  return HttpResponse(template.render(context, request))
  
def create_intern(request):
    if request.method == "POST":
        try:
            # Load the data from the POST request body
            data = json.loads(request.body)
            
            # Create a new intern object with the provided data
            intern = interns.objects.create(
                name=data.get("name"),
                email=data.get("email"),
                age=data.get("age"),
                salary=data.get("salary")  
            )
            print(request.COOKIES)
            # Return the newly created intern as a JSON response
            return JsonResponse({
                "id": intern.id,
                "name": intern.name,
                "email": intern.email,
                "age": intern.age,
                "salary": intern.salary,
            }, status=201)
            # return HttpResponseRedirect(reverse('get_all_person'))
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)
 

def insert_intern(request):

  template = loader.get_template('post.html')
  
  return HttpResponse(template.render())