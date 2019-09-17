from django.contrib.auth.models import User

admin = User.objects.create_user('admin', password='Admin2019')
admin.is_superuser = True
admin.is_staff = True
admin.save()

Bob = User.objects.create_user('Bob', password='Bob2019')
Bob.is_superuser = False
Bob.is_staff = False 
Bob.save()

Alice = User.objects.create_user('Alice', password='Alice2019')
Alice.is_superuser = False
Alice.is_staff = False 
Alice.save()

