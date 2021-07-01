"""A video player class."""

from .video_library import VideoLibrary
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.playing = ""
        self.paused = False
        self.playlists = {}
        self.lists_orig = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        videos = []
        for video in self._video_library.get_all_videos():
            videos += [video.title+" ("+video.video_id+") ["+" ".join(video.tags)+"]"]
        videos.sort()

        print("Here's a list of all available videos:")
        for video in videos: print(video)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video:
            if self.playing:
                print("Stopping video: " + self._video_library.get_video(self.playing).title)
            self.playing = video.video_id
            self.paused = False
            print("Playing video: "+video.title)
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self.playing:
            video = self._video_library.get_video(self.playing).title
            self.playing = ""
            self.paused = False
            print("Stopping video: "+video)
        else:
            print("Cannot stop video: No video is currently playing")


    def play_random_video(self):
        """Plays a random video from the video library."""
        random_id = random.choice(self._video_library.get_all_videos()).video_id
        self.play_video(random_id)

    def pause_video(self):
        """Pauses the current video."""
        if self.playing:
            video = self._video_library.get_video(self.playing).title
            if self.paused:
                print("Video already paused: "+video)
            else:
                self.paused = True
                print("Pausing video: "+video)
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.playing:
            video = self._video_library.get_video(self.playing).title
            if self.paused:
                self.paused = False
                print("Continuing video: "+video)
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        if self.playing:
            video = self._video_library.get_video(self.playing)
            video = video.title + " (" + video.video_id + ") [" + " ".join(video.tags) + "]"
            if self.paused:
                video += " - PAUSED"
            print("Currently playing: "+video)
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in list(self.playlists):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlists[playlist_name.upper()] = []
            self.lists_orig.append(playlist_name)
            self.lists_orig.sort(key = lambda x: x.lower())
            print("Successfully created new playlist: "+playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        deny = "Cannot add video to "+playlist_name+": "
        if playlist_name.upper() in list(self.playlists):
            if video_id in self.playlists[playlist_name.upper()]:
                print(deny+"Video already added")
            else:
                video = self._video_library.get_video(video_id)
                if video:
                    self.playlists[playlist_name.upper()].append(video_id)
                    print("Added video to "+playlist_name+": "+video.title)
                else:
                    print(deny+"Video does not exist")
        else:
            print(deny+"Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        if self.lists_orig:
            print("Showing all playlists:")
            for name in self.lists_orig:
                print("  "+name)
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in list(self.playlists):
            print("Showing playlist: "+playlist_name)
            playlist = self.playlists[playlist_name.upper()]
            if playlist:
                for vid_id in playlist:
                    video = self._video_library.get_video(vid_id)
                    print("  "+video.title + " (" + video.video_id + ") [" + " ".join(video.tags) + "]")
            else:
                print("  No videos here yet")
        else:
            print("Cannot show playlist "+playlist_name+": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        deny = "Cannot remove video from "+playlist_name+": "
        if playlist_name.upper() in list(self.playlists):
            playlist = self.playlists[playlist_name.upper()]
            if video_id in playlist:
                playlist.remove(video_id)
                print("Removed video from "+playlist_name+": "+self._video_library.get_video(video_id).title)
            elif self._video_library.get_video(video_id):
                print(deny+"Video is not in playlist")
            else:
                print(deny+"Video does not exist")
        else:
            print(deny+"Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in list(self.playlists):
            self.playlists[playlist_name.upper()] = []
            print("Successfully removed all videos from "+playlist_name)
        else:
            print("Cannot clear playlist "+playlist_name+": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in list(self.playlists):
            del self.playlists[playlist_name.upper()]
            self.lists_orig = [name for name in self.lists_orig if name.upper() != playlist_name.upper()]
            print("Deleted playlist: "+playlist_name)
        else:
            print("Cannot delete playlist "+playlist_name+": Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        lookup = {video.title:video for video in videos}
        videos = [video.title for video in videos]
        videos = [video for video in videos if search_term.upper() in video.upper()]
        videos.sort()
        results = {}
        for i in range(len(videos)):
            video = lookup[videos[i]]
            results[i+1] = ["  "+str(i+1)+") "+video.title+" ("+video.video_id+") ["+" ".join(video.tags)+"]",video]
        if results:
            print("Here are the results for "+search_term+":")
            for result in list(results.values()):
                print(result[0])
            s1 = "Would you like to play any of the above? "
            s2 = "If yes, specify the number of the video.\n"
            s3 = "If your answer is not a valid number, we will assume it's a no.\n"
            command = input(s1+s2+s3)
            try:
                self.play_video(results[int(command)][1].video_id)
            except:
                pass
        else:
            print("No search results for "+search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
