from music.models import Album, SongsInAlbum
from rest_framework import serializers
from django.db.models import Count

class AlbumSerializer(serializers.ModelSerializer):
    total_songs = serializers.SerializerMethodField()
    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ['id','total_likes', 'artist_id', 'total_songs']
    
    def validate(self, attrs):  ## checks if the album name already exists or not
        try:
            if Album.objects.filter(album_name = attrs['album_name']).exists():
                raise serializers.ValidationError("Album already exists")
            return attrs
        except Exception as e:
            raise serializers.ValidationError(str(e)) 
            
    def get_total_songs(self, attrs):   ## returns a list of count of songs in each album of an artist
        total_songs_in_each_album = attrs.filter(id = attrs.id, artist_id = attrs.artist_id)
        # return [i.count() for i in total_songs_in_each_album]
        total_songs_in_each_album = total_songs_in_each_album.values('id').annotate(total_songs=Count('id'))

        # Extracting the counts into a list
        return [album['total_songs'] for album in total_songs_in_each_album]        

class SongsInAlbumSerializer(serializers.ModelSerializer):
    total_songs = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()
    class Meta:
        model = SongsInAlbum
        fields = '__all__'
        read_only_fields = ['id','song_id','album_id','total_songs']
        
    def get_total_songs(self, attrs):   ## total songs in an album
        songs_in_album = attrs.album_id 
        # songs_in_album = attrs.album_id.songs.all()
        return songs_in_album.count()
                                                                                                                                    