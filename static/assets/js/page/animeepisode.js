// Assigning Buttons
var remove_Button = document.getElementById('remove_Button');
var WatchingButton = document.getElementById('WatchingButton');
var CompletedButton = document.getElementById('CompletedButton');

function removeAnime(anime_Id){

    remove_Button.disabled = true;

    Swal.fire({
        title: "Remove Anime?",
        text: "Do you want to remove this anime to the list?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Remove on my List"
      }).then((result) => {
        if (result.isConfirmed) {

            notyf.open({message: "Removing Anime, Please Wait...", background: 'violet', duration: 0});

            // Construct the URL with query parameters
            const url = `/backend/backend/RemoveAnime2/${anime_Id}`;

            // Redirect to the constructed URL
            window.location.href = url;

        } else {
            remove_Button.disabled = false;
        }
    });
}

function episodeWatching(episode_Id){

    WatchingButton.disabled = true;

    Swal.fire({
        title: "Currently Watching?",
        text: "Do you want to update this episode?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Update"
      }).then((result) => {
        if (result.isConfirmed) {

            notyf.open({message: "Updating, Please Wait...", background: 'violet', duration: 0});

            // Construct the URL with query parameters
            const url = `/backend/backend/WatchingEpisode/${encodeURIComponent(episode_Id)}`;

            // Redirect to the constructed URL
            window.location.href = url;

        } else {
            WatchingButton.disabled = false;
        }
    });
}

function episodeCompleted(episode_Id){

    CompletedButton.disabled = true;

    Swal.fire({
        title: "Completed Watching?",
        text: "Do you want to update this episode?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Update"
      }).then((result) => {
        if (result.isConfirmed) {

            notyf.open({message: "Updating, Please Wait...", background: 'violet', duration: 0});

            // Construct the URL with query parameters
            const url = `/backend/backend/CompletedEpisode/${encodeURIComponent(episode_Id)}`;

            // Redirect to the constructed URL
            window.location.href = url;

        } else {
            CompletedButton.disabled = false;
        }
    });
}