from django.contrib import admin

# Register your models here.
from . models import Event
admin.site.register(Event)



from . models import feedback
admin.site.register(feedback)

from . models import Owner
admin.site.register(Owner)

from . models import eventsupdates
admin.site.register(eventsupdates)

from . models import Utensilsform
admin.site.register(Utensilsform)

from . models import refund
admin.site.register(refund)

from . models import deccart
admin.site.register(deccart)

from . models import chef
admin.site.register(chef)

from . models import Transaction
admin.site.register(Transaction)

from . models import decorationtransaction
admin.site.register(decorationtransaction)

from . models import icart
admin.site.register(icart)

from . models import Paymentd
admin.site.register(Paymentd)

from . models import Payment
admin.site.register(Payment)