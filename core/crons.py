from .models import *


def give_daily_tip():
  tips = Tip.objects.order_by('order').all()
  tutors = User.objects.all()

  for tutor in tutors:
    if tutor.tip_of_day is None or tutor.tip_of_day.order == tips.last().order:
      tutor.tip_of_day = tips.first()
    else:
      tutor.tip_of_day = tips.filter(order=tutor.tip_of_day.order + 1).first()

    tutor.save()
