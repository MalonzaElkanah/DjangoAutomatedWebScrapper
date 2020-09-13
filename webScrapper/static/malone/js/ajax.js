/*
Author       : ElkanahMalonza
App name     : Malone
Version      : 1.0
*/
(function($) {
	/*
	template: auth-login.html
	server  : malone/views.py
	*/
	$("#id_login-form").submit(function(event) {
       	event.preventDefault();
       	$.ajax({ 
       		data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
	            console.log(response);
	            if(response['success']) {
		            //$("#feedbackmessage").html("<div class='alert alert-success'>Succesfully sent feedback, thank you!</div>");
		            //$("#feedbackform").addClass("hidden");
		            window.location.href = "../";
	            }
	            if(response['error']) {
	            	alert(response['error']);
	            	$("#id_error-text").html("Error: "+response['error']+"");
	            }
        	},
	        error: function (request, status, error) {
	            console.log(request.responseText);
	        }
       	});
   	});

/*
	//<input type="hidden" id="ids" name="ids" value="{{doc_profile.id}}">
	$('#id_fav-btn').click(function(event){
		event.preventDefault();
		var id = $("input[name='ids']").val();
		var csrf = $("input[name='csrfmiddlewaretoken']").val();
		var p_data = {
			doc_id: id,
			csrfmiddlewaretoken: csrf,
		};
		var serializedData = $(this).serialize();
		//csrfmiddlewaretoken
		var link = '../../toggle-favourite/'+id+'/';

		$.ajax({
            type: 'GET',
            url: ""+link+"",
            data: serializedData,
            success: function (response) {
		        alert(response["responseJSON"]);	
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response);
            }
        })
	}); */
})(jQuery);