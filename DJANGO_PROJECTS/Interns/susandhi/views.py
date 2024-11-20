from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from django.http import HttpResponse ,JsonResponse,HttpResponseNotAllowed
from django.template import loader
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def Main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def get_all_person(request):
    latest_intern=interns.objects.all()
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
        Intern = interns.objects.all()
        response_data = []
        for intern in Intern:
            response_data.append({
                'id': intern.id,
                'name': intern.name,
                'email': intern.email,
                'age': intern.age,
                'salary': intern.salary,
            })
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
@csrf_exempt
def delete_intern(request,id):
  
    if request.method == "DELETE":
        try:
            # Retrieve the interns object by id
            intern = get_object_or_404(interns, id=id)
            
            # Delete the interns
            intern.delete()
            
            # Return a success response
            return JsonResponse({"message": f"interns  deleted successfully","Status":True}, status=200)
        
        except Exception as e:
            #  return an error response
            return JsonResponse({"error": f"An error occurred: {str(e)}","Status":False}, status=500)
    
    # Return method not allowed if the request is not DELETE
    return HttpResponseNotAllowed(["DELETE"], "Method not allowed")


def delete(request, id):
  if request.method == 'DELETE':
      item = get_object_or_404(interns, id=id)
      item.delete()
      return JsonResponse({'message': 'Item deleted successfully!'}, status=200)
  else:
      return JsonResponse({'message': 'Invalid method'}, status=405)

@csrf_exempt
def update(request, id):
    if request.method == 'PUT':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)  # Parse the request body

            # Get the interns object to be updated
            intern = get_object_or_404(interns, id=id)

            # Update fields if they are present in the request data
            name = data.get('name', intern.name) 
            age=data.get('age', intern.age) 
            salary = data.get('salary', intern.salary) 
            
            intern.name = name
            intern.salary = salary
            intern.age=age
           
            intern.save()

            
            # Return success response
            return JsonResponse({'message': 'interns updated successfully!', "Status":True}, status=202)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data',"Status":False}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    # If the request method is not PUT
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

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

            Name = data.get("name", "").strip()
            Email = data.get("email", "").strip()
            Age = int(data.get("age", 0))
            Salary = int(data.get("salary", 0))

            # Create a new interns object with the provided data
            intern= interns.objects.create(
                name=Name,
                email=Email,
                age=Age,
                salary=Salary
            )

            # Return the newly created interns as a JSON response
            return JsonResponse({
                "Message": "Employ created Successfully",
                "Status":True
            }, status=201)
            
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format","Status":False}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)
 


 

def insert_intern(request):

  template = loader.get_template('post.html')
  
  return HttpResponse(template.render())

def filter_person(request):
    # Get the name parameter from the GET request (if it exists)
    name_filter = request.GET.get('name', '')

    # If a name was provided, filter the internees by that name (case-sensitive)
    if name_filter:
        mydata = interns.objects.filter(name__contains=name_filter)  
    else:
        mydata = "" 
    return render(request, 'filter_person.html', {'mymember': mydata, "all": interns.objects.all()})
