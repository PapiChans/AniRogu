(function () {
    'use strict';

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation');

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(function (form) {
        // Track if the form has been submitted
        var submitted = false;

        // Disable the submit button initially
        var submitButton = form.querySelector('[type="submit"]');
        submitButton.disabled = true;

        form.addEventListener('input', function () {
            // Enable the submit button if the form is valid and not yet submitted
            if (form.checkValidity() && !submitted) {
                submitButton.disabled = false;
            } else {
                submitButton.disabled = true;
            }
        });

        form.addEventListener('submit', function (event) {
            // Prevent multiple submissions
            if (submitted) {
                event.preventDefault();
                return;
            }

            submitted = true;

            // Disable the submit button immediately on form submission
            submitButton.disabled = true;

            // Validate the form
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        }, false);
    });
})();