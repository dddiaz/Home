
$(function(){
    //Formspree Setup
    var $contactForm = $('#contact-form');
    $contactForm.submit(function(e) {
        //alert("Submitting");
        e.preventDefault();
        $.ajax({
            url: '//formspree.io/daniel.delvin.diaz@gmail.com',
            method: 'POST',
            data: $(this).serialize(),
            dataType: 'json',
            beforeSend: function() {
            },
            success: function(data) {
                //$contactForm.find('#contact-form').hide();
                //$(this).closest('form').find("input[type=text], textarea").val("");
                $("#contact-submit-btn").hide();
                $contactForm.append('<div class="">Message sent! I will get back to you shortly!</div>');
            },
            error: function(err) {
                $contactForm.append('<div class=""> Dang it, there was an error. Make sure you filled out the fields and please try again.</div>');
            }
        });
    });
});
