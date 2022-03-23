from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from library.models import Court, FavCourt

class FavCourtView(APIView):
    def post(self, request, format=None):
        try:
            user = request.user
        except:
            return Response({ 'success': 0, 'message': 'User is not authenticated' })
        
        else:
            try:
                data = request.data
                court_slug = data['slug']
                court_user_partner = data['user_partner']
            except:
                return Response({ 'success': 0, 'message': 'Data is incomplete' })

            else:
                try:
                    court = Court.objects.get(user_partner__username=court_user_partner, slug=court_slug)
                except:
                    return Response({ 'success': 0, 'message': 'Court does not exist' })

                else:
                    if FavCourt.objects.filter(user=user, court=court).exists():
                        return Response({ 'success': 0, 'message': 'The court is already a favorite for user' })
                    else:
                        try:
                            fav_court = FavCourt(user=user, court=court)
                            fav_court.save()

                            return Response({ 'success': 1, 'message': 'Court has been added to favorite' })
                        except:
                            return Response({ 'success': 0, 'message': 'Something went wrong when saving court to favorite' })
            
    def delete(self, request, format=None):
        try:
            user = request.user
        except:
            return Response({ 'success': 0, 'message': 'User is not authenticated' })
        else:
            try:
                data = request.data
                print(data)
                court_slug = data['slug']
                court_user_partner = data['user_partner']
            except:
                return Response({ 'success': 0, 'message': 'Data is incomplete' })
            else:
                try:
                    court = Court.objects.get(user_partner__username=court_user_partner, slug=court_slug)
                except:
                    return Response({ 'success': 0, 'message': 'Court does not exist' })

                else:
                    FavCourt.objects.filter(user=user, court=court).delete()

                    return Response({ 'success': 1, 'message': 'Court has been deleted from favorite' })


# Ajax request for get all favorite court
class FavCourtSerializer(serializers.ModelSerializer):    
    court_title = serializers.CharField(source='court.title')
    court_img = serializers.ImageField(source='court.img1')    
    court_type = serializers.CharField(source='court.type.name')
    court_rate = serializers.IntegerField(source='court.rate')
    court_address = serializers.CharField(source='court.user_partner.address')
    user_partner = serializers.CharField(source='court.user_partner.username')
    slug = serializers.SlugField(source='court.slug')

    class Meta:
        model = FavCourt
        fields = ['court_title', 'court_img', 'court_type', 'court_rate', 'court_address', 'user_partner', 'slug']


class GetFavCourtView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
        except:
            return Response({ 'error': 'User is not authenticated' })
        
        else:
            try:
                fav_courts = FavCourt.objects.filter(user=user)

                serializer = FavCourtSerializer(fav_courts, many=True)

                return Response(serializer.data)
            
            except:
                return Response({ 'error': 'Something went wrong when retrieving favorite court data' })
