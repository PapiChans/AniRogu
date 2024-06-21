// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {

          var submitButton = form.querySelector('[type="submit"]');
          submitButton.disabled = true;

          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
          // Optionally, you can enable the submit button after a delay or some other condition
          // For example, enable after 3 seconds
          setTimeout(function() {
            submitButton.disabled = false;
          }, 1000); // Adjust the delay as needed

        }, false)
      })
  })()