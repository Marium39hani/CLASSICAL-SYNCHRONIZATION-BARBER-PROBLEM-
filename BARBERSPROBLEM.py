from threading import Thread
import threading
import time
import random

barber_wakeup = 1 #1 indicates that customer can wake up the barber
customers_sem = threading.Semaphore(0)
barber_sem = threading.Semaphore(0)
mutex = threading.Semaphore(1) #Mutual Exclusion

class BarberShop:
     waiting_customers = []

     def __init__(self,barber,total_chairs):
         self.barber = barber
         self.total_chairs = total_chairs
         print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
         print("The Bareber Shop is Opening!")
         print("The Barber Shop contains:", total_chairs,"waiting seats")
         print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")

     def startBarberThread(self):
         t_barber = Thread(target = self.barber_working_in_barber_room)
         t_barber.start()

     def barber_shop_entry(self,customer):
         print("\nCustomer {} is entering in the shop and looking for empty seats.".format(customer))
         mutex.acquire() #Try to get access to the waiting room chairs or Enter in CS
                         #if waiting room is not full then customer can sit on chair
         if len(self.waiting_customers) < self.total_chairs:
             print("\nCustomer {} finds an empty chair.".format(customer))
             self.waiting_customers.append(customer)
             global barber_wakeup
             while barber_wakeup:
                     #barber gets a wakeup call by a customer
                 customers_sem.release() #1st customer will come
                 print("\nCustomer {} wakes up the barber.".format(customer))
                 barber_wakeup = 0 #now no customer can wakeup the baber before barber goes to sleep

             print("Customer {} sits on the waiting chair.".format(customer))
             mutex.release() #customer after sitting on waiting seat is releasing the lock

             print("\nCustomer {} is waiting to be called by the barber.".format(customer))
             barber_sem.acquire()
             Customer.get_hair_cut(self,customer) #customer is having haircut

         else: #if waiting room is full
             #As no seat is empty so leaving the CS
             mutex.release()
             Customer.balk(self,customer)
     def barber_working_in_barber_room(self):
         while True:
                     #if there are no customer to be served in waiting room
             if len(self.waiting_customers) == 0:
                 global barber_wakeup
                 print("Barber is sleeping and waiting for a customer to wake him up.")
                 barber_wakeup = 1 #now customer can wakeup barber
                 customers_sem.acquire() #barber sleeps if there is no customer

                 #if customers are waiting in the room
             if len(self.waiting_customers) > 0:
                 mutex.acquire() #Barber sees the customer so he locks the barber's chair (CS)
                                  #Barber calls the customer
                 cust = self.waiting_customers[0]
                 print("\nBarber calls {} for a haircut.".format(cust))
                 time.sleep(1)
                 del self.waiting_customers[0]
                 barber_sem.release() #barber is now ready to work
                 mutex.release() #Barber unlocks the barber's chair so that the customer have the chair
                 self.barber.cut_hair(cust) #Hair Cutting


class Barber:
    
     def cut_hair(self,customer):
         for i in range(0,1):
             print("\nBarber is cutting {}'s hair.".format(customer))
             time.sleep(5)
         print("\n{} is done so leaving the barber shop.".format(customer))


class Customer:

     def __init__(self,name):
         self.name = name

     def get_hair_cut(self,customer):
         for i in range(0,1):
             print("\nCustomer {} is having a haircut".format(customer))
             time.sleep(2)
     def balk(self,customer):
         print("\nWaiting Room is full. The recently arrived customer {} leaves barber shop without hair cutting.".format(customer))

if __name__ == '__main__':
     
     customers_list = []
     CustLimit=int(input("Enter total customers that are going to arrive in the Barber shop:"))
     seatNo=int(input("Enter total Number of waiting Seats:"))
     for i in range(CustLimit):
         CustName=input("Enter names of the upcoming customers for the barber shop: ")
         customers_list.append(Customer(CustName))
     barber = Barber()

     barberShop = BarberShop(barber, seatNo) 
     barberShop.startBarberThread()

     while len(customers_list) > 0:
         c = customers_list.pop()
 #running customer threads here
         t = threading.Thread(target = barberShop.barber_shop_entry, args = (c.name,))
         time.sleep(random.randint(4,8)) #customers are entering in shop time by time
         t.start()
