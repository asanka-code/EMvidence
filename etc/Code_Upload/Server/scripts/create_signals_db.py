from django.utils import timezone
import random
from signals.models import *
from datetime import datetime

from django.contrib.auth.models import User
from signals.models import SignalTag
# Users
admin = User.objects.get(username='admin')
bob = User.objects.get(username='Bob')
alice = User.objects.get(username='Alice')

# Tags
available_tags = [stag.name for stag in SignalTag.objects.all()]
print(f"Available Tags: {available_tags}")

for user in [bob, alice]:
    num_signals = random.randint(1, 5)
    for i in range(num_signals):

        s = Signal(owner=alice, public=True, core_description=f"{user.username} Signal {i}")
        s.save()

        print(f"Created Signal[{s.uuid}]: {s}")

        # Add random captures and corresponding annotations
        num_captures = random.randint(1, 4)
        for j in range(num_captures):
            c = Capture(signal=s, core_time=datetime.now(), core_sample_start=j, core_sampling_rate=8000000, core_frequency=18000000)
            c.save()

            a = Annotation(signal=s, core_sample_start=j, core_sample_count=(random.randint(2,10)*1024), core_comment=f"Annotation {j} in {s}")
            a.save()

            print(f"     Signal[{s}]: {c}")

        # Add 2 random tags
        tags_selected = random.sample(available_tags, 2)
        for random_tag in tags_selected:
            tag_object = SignalTag.objects.filter(name=random_tag).first()
            s.tag.add(tag_object)
            print(f"     Signal[{s}]: {random_tag}")

# s = Signal(owner=alice, public=False, core_description="Alice Public Signal 1")
# s.save()
# des = s.core_description
# s = Signal.objects.filter(core_description=des)
# Signal.objects.filter(core_description=des).first()
#
# s = Signal.objects.get(core_description="Alice Private Signal 1")
# s = Signal.objects.get(pk=1)
#
# c = Capture(signal=s, core_time=datetime.now(), core_sample_start=0, core_sampling_rate=8000000, core_frequency=18000000)
# c.save()
#
# print(Capture.objects.all())