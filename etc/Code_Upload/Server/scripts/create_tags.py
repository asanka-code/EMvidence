from signals.models import SignalTag

for i in ["Crime Scene", "Education/Training", "IoT", "Demo", "Research", "Embedded", "Cryptography"]:
    tag = SignalTag(name=i)
    tag.save()
