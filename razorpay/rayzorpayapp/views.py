import os
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from razorpay import Client
from .models import Order,Refund
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")
def OrderView(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        name = request.POST.get('name')
        client = Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))
        order_data = {
            'amount': int(amount * 100),  # Convert to paise
            'currency': 'INR',
            'receipt': name,
        }
        order = client.order.create(data=order_data)
        Order.objects.create(order_id=order['id'], amount=amount, name=name)
        return redirect('payment', order_id=order['id'])
        # return HttpResponse('Order Details added successfully')
    template_name = 'razor/create_order.html'
    context = {}
    return render(request, template_name, context)



@csrf_exempt
def paymentView(request, order_id):
    order = Order.objects.get(order_id=order_id)
    print('order',Order.objects.all())
    return render(request, 'razor/payment.html', {'order': order})


@csrf_exempt
def successView(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
    }

    client  = Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        razorpay_save = Order.objects.get(
            order_id=response['razorpay_order_id'])
        razorpay_save.razorpay_payment_id = response['razorpay_payment_id']
        razorpay_save.razorpay_signature = response['razorpay_signature']
        razorpay_save.paid = True
        razorpay_save.save()

        return render(request, 'razor/success.html', {'status': status})
    except Exception as e:
        return render(request, "razor/success.html", {'status': False})

def showView(request):

    try:
        
        #data =Order.objects.filter(paid=True).values()
            data = Order.objects.all()

            return render(request, 'razor/datadisplay.html', {'data': data})
    except Exception as e:


        return render(request, 'razor/datadisplay.html', {'data': 'insufficient data'})





def initiate_refund(request,order_id):
    try:
        order = get_object_or_404(Order, order_id=order_id)
        print('--------------------',order)

        client = Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))
        print('client',client)
        refund_data = {

            'amount': int(order.amount * 100),  # Refund amount in paise


        }

        refund = client.payment.refund(order.razorpay_payment_id, refund_data['amount'])

        Refund.objects.create(order=order, refunded_amount=order.amount, reason="Customer request",refund_id=refund['id'])
        print('refund_id',refund['id'])
        return HttpResponse('Your amount refund successfully')
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    finally:
        return redirect('create_order')
