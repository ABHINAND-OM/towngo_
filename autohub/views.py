from django.contrib import messages
from django.contrib.admin.utils import unquote
from django.shortcuts import render, redirect, get_object_or_404

from autohub.models import hubRegistration, Mechanic
from django.contrib.auth import authenticate, login, logout
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import ACos, Cos, Radians, Sin

from loginregister.models import UserDetail
from user_re.models import ServiceRequest
from django.http import Http404, HttpResponseNotFound, JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def hubcollection(request):
    if request.method == 'POST':
        user_latitude = request.POST.get('user_latitude')
        user_longitude = request.POST.get('user_longitude')

        # If user provides location, find the nearest hub
        if user_latitude and user_longitude:
            nearest_autohub = get_nearest_autohub(user_latitude, user_longitude)
            return render(request, 'nearest_autohub.html', {'nearest_autohub': nearest_autohub,
                                                            'user_latitude': user_latitude,
                                                            'user_longitude': user_longitude})

    # Fetch all hubs from the database
    hublist = hubRegistration.objects.all()

    # Pass the hubs list to the template
    context = {
        'hubs': hublist,
    }

    # Render the template with the context
    return render(request, 'hubcollection.html', context)


def get_nearest_autohub(user_latitude, user_longitude):
    # Convert user inputs to float
    user_latitude = float(user_latitude)
    user_longitude = float(user_longitude)

    # Calculate distance using Haversine formula
    autohubs = hubRegistration.objects.annotate(
        distance=ExpressionWrapper(
            ACos(
                Sin(Radians(user_latitude)) * Sin(Radians(F('latitude'))) +
                Cos(Radians(user_latitude)) * Cos(Radians(F('latitude'))) *
                Cos(Radians(F('longitude')) - Radians(user_longitude))
            ) * 6371,  # Earth radius in kilometers
            output_field=fields.FloatField()
        )
    ).order_by('distance')[:1]

    if autohubs:
        return autohubs[0]

    return None


# Create your views here.
# def hubregister(request):
#     if request.method == 'POST':
#         selected_hub_types = request.POST.getlist('hubtype')
#
#         workshopname = request.POST['workshopname']
#         email = request.POST['email']
#         mobilenumber = request.POST['mobilenumber']
#         telephonenumber = request.POST['telephonenumber']
#         address = request.POST['address']
#         operatinghr = request.POST['operatingHours']
#         ab = request.FILES.get("hubimg")
#         # hubimg = request.POST['hubimg']
#         latitude = request.POST['latitude']
#         longitude = request.POST['longitude']
#
#         password = request.POST['password']
#         cpassword = request.POST['cpassword']
#
#         hub_detail = hubRegistration(Hub_name=workshopname, email=email, mobile_number=mobilenumber,
#                                      telephone_number=telephonenumber, address=address, operating_hours=operatinghr,
#                                      hub_types=selected_hub_types, hub_image=ab, latitude=latitude,
#                                      longitude=longitude,
#                                      password=password)
#         hub_detail.save()
#         print("hub created")
#
#     return render(request, 'hubregister.html')


# def hublogin(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user3 = hubRegistration.objects.filter(email=email, password=password)
#
#         if user3 is not None:
#             print('loggedin')
#             # login(request, user3)
#             # Redirect to a success page or the user's dashboard
#             return redirect('hubindex')  # Replace 'dashboard' with the actual URL name for the user's dashboard
#
#         else:
#             # Authentication failed, show an error message
#             error_message1 = "Invalid email or password."
#             return render(request, 'hublogin.html', {'error_message1': error_message1})
#     return render(request, 'hublogin.html')



def hubregister(request):
    if request.method == 'POST':
        selected_hub_types = request.POST.getlist('hubtype')
        workshopname = request.POST['workshopname']
        email = request.POST['email']
        mobilenumber = request.POST['mobilenumber']
        telephonenumber = request.POST['telephonenumber']
        address = request.POST['address']
        operatinghr = request.POST['operatingHours']
        hubimg = request.FILES.get("hubimg")
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # Validate password length using Django's built-in validator
        try:
            validate_password(password)
        except ValidationError as e:
            msg = e.messages[0]  # Show the first error message
            messages.error(request, msg)
            return render(request, 'hubregister.html')

        # Check if the email is already taken
        if hubRegistration.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return render(request, 'hubregister.html')

        if password == cpassword:
            hub_detail = hubRegistration(
                Hub_name=workshopname,
                email=email,
                mobile_number=mobilenumber,
                telephone_number=telephonenumber,
                address=address,
                operating_hours=operatinghr,
                hub_types=selected_hub_types,
                hub_image=hubimg,
                latitude=latitude,
                longitude=longitude,
                password=password
            )
            hub_detail.save()
            messages.success(request, "Hub registration successful.")
            return render(request, 'hubregister.html')  # You can redirect to a success page if needed

        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'hubregister.html')

    return render(request, 'hubregister.html')
def hublogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Use get instead of filter since you expect a single user
            hub_user = hubRegistration.objects.get(email=email, password=password)
        except hubRegistration.DoesNotExist:
            # Authentication failed, show an error message
            error_message1 = "Invalid email or password."
            return render(request, 'hublogin.html', {'error_message1': error_message1})

        # Authentication successful, set a session variable or other custom logic if needed
        request.session['hub_email'] = hub_user.email
        print('loggedin')
        request.session['id'] = hub_user.id
        return redirect('hubindex')

    return render(request, 'hublogin.html')


def hubindex(request):
    id = request.session['id']
    requestss = ServiceRequest.objects.filter(idno=id)

    print(requestss)

    return render(request, 'hubindex.html', {'requestss': requestss})


def hubprofile(request):
    # Check if the hub is authenticated (hub_email is in the session)
    if 'hub_email' in request.session:
        # Retrieve hub details based on the authenticated email
        hub_details = hubRegistration.objects.get(email=request.session['hub_email'])
        print('Hub Image URL:', hub_details.hub_image.url)
        return render(request, 'hubprofile.html', {'hub_details': hub_details})
    else:
        # Redirect or handle the case when the hub is not authenticated
        return redirect('hublogin')


def hubprofileedit(request):
    return render(request, 'hubprofileedit.html')


# def add_mechanic(request):
#     if request.method == 'POST':
#         # Get the data from the form
#         name = request.POST['name']
#         phone_number = request.POST['phone_number']
#
#         # Get the currently logged-in hub
#
#         # Create a new Mechanic object associated with the hub
#         mechanic = Mechanic.objects.create(
#             name=name,
#             phone_number=phone_number,
#
#         )
#         mechanic.save()
#
#         # Redirect to a success page or do any additional logic
#         return redirect('hubindex')
#
#     return render(request, 'add_mechanic.html')

def add_mechanic(request):
    if request.method == 'POST':
        # Get the data from the form
        name = request.POST['name']
        phone_number = request.POST['phone_number']

        # Get the currently logged-in hub from the session
        hub_id = request.session.get('id')
        if hub_id is None:
            # Handle the case where there is no logged-in hub
            return redirect('hublogin')  # Redirect to login page or handle it as appropriate

        # Get the hub object
        hub = hubRegistration.objects.get(id=hub_id)

        # Create a new Mechanic object associated with the hub
        mechanic = Mechanic.objects.create(
            name=name,
            phone_number=phone_number,
            hub=hub,
        )
        mechanic.save()

        # Redirect to a success page or do any additional logic
        return redirect('hubindex')

    return render(request, 'add_mechanic.html')


def mechanic_list(request):
    hub_id = request.session.get('id')
    hub = hubRegistration.objects.get(id=hub_id)

    mechanics = Mechanic.objects.filter(hub=hub)
    return render(request, 'mechanic_details.html', {'mechanics': mechanics})


def assign_mechanic(request, request_id):
    if request.method == 'POST':
        # Get the selected mechanic ID from the form
        mechanic_id = request.POST.get('mechanic')

        # Add print statements to debug
        print(f"Request ID: {request_id}, Mechanic ID: {mechanic_id}")

        # Get the request and mechanic objects
        service_request = ServiceRequest.objects.get(id=request_id)

        try:
            mechanic = Mechanic.objects.get(id=mechanic_id, hub=request.user.hub)
        except Mechanic.DoesNotExist:
            print(f"Mechanic with ID {mechanic_id} does not exist for the current hub.")
            return HttpResponseNotFound("Mechanic not found.")

        # Assign the mechanic to the request (update your ServiceRequest model accordingly)
        service_request.mechanic = mechanic
        service_request.save()

        # Redirect to a success page or do additional logic
        return redirect('hubindex')

    # Get the list of available mechanics for the current hub
    mechanics = Mechanic.objects.filter(hub=request.user.hub)

    # Pass the mechanics and request ID to the template
    context = {'mechanics': mechanics, 'request_id': request_id}
    return render(request, 'assign_mechanic.html', context)


def delete_request(request, id):
        id=id
        mechanic = get_object_or_404(Mechanic, id=id)
        mechanic.delete()
        return redirect('mechanic_list')


def hublogout(request):
    logout(request)
    return redirect('index')
