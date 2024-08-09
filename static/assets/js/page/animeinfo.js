// Assigning Buttons
var add_Button = document.getElementById('anime_Add');
var remove_Button = document.getElementById('anime_Remove');

// Assigning Variables
const add_context = {
    anime_number: anime_Number,
    anime_name: anime_Name,
    anime_picture: anime_Picture
};

// Function to convert object to query string
function toQueryString(obj) {
    return Object.keys(obj)
        .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(obj[key]))
        .join('&');
}

function addAnimeClick(){

    add_Button.disabled = true;

    Swal.fire({
        title: "Add Anime?",
        text: "Do you want to add this anime to the list?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Add on my List"
      }).then((result) => {
        if (result.isConfirmed) {
            // Convert context object to query string
            const queryString = toQueryString(add_context);

            // Construct the URL with query parameters
            const url = `/backend/backend/AddAnime?${queryString}`;

            // Redirect to the constructed URL
            window.location.href = url;
        } else {
            add_Button.disabled = false;
        }
    });
}

function removeAnimeClick(){

    remove_Button.disabled = true;

    Swal.fire({
        title: "Remove Anime?",
        text: "Do you want to remove this anime to the list?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Add on my List"
      }).then((result) => {
        if (result.isConfirmed) {
            // Convert context object to query string
            const queryString = toQueryString(add_context);

            // Construct the URL with query parameters
            const url = `/backend/backend/RemoveAnime?${queryString}`;

            // Redirect to the constructed URL
            window.location.href = url;
        } else {
            remove_Button.disabled = false;
        }
    });
}