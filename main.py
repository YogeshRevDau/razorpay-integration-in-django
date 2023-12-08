
import razorpay
client = razorpay.Client(auth=("rzp_test_WAWBpAueqop6CP", "493rcv72keb778fnZj0WDvsV"))

order_data=client.order.create({
  "amount": 50000,
  "currency": "INR",
  "receipt": "Yogesh",
  "notes": {
    "key1": "value3",
    "key2": "value2"
  }
})

# print(order_data)
