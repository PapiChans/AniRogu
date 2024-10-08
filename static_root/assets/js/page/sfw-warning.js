function swfButton() {
    Swal.fire({
        title: "Mature content",
        text: "You must at least 18 years old to continue.",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "I am 18 or older"
      }).then((result) => {
        if (result.isConfirmed) {

            notyf.open({message: "Directing...", background: 'violet', duration: 0});

            const url = `/user/h/home`;

            // Redirect to the constructed URL
            window.location.href = url;
        }
    });
}