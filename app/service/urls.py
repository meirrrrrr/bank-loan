from rest_framework import routers
from app.service.views import ProgramViewSet


router = routers.DefaultRouter()
router.register('v1/program', ProgramViewSet)

app_name = 'service'
urlpatterns = router.urls
