(function($) {
    "use strict";
    // Add Milestone Add More
    
    $(".site-info").on('click','.trash', function () {
        $(this).closest('.site-cont').remove();
        return false;
    });

    $(".add-site").on('click', function () {
 
        var input_num = parseInt($("#count").text());
        input_num = input_num + 1;
        $("#count").text(''+input_num+'');
        $("input[name='form_num']").val(''+input_num+'');
        var listcontent = '<div class="row form-row site-cont">' +
            '<div class="col-12 col-md-5">' +
                '<div class="form-group">' +
                    '<label>Data Url</label>' +
                    '<input type="text" class="form-control" name="url_scrapped_'+input_num+'">' +
                '</div>' +
            '</div>' +
            '<div class="col-12 col-md-5">' +
                '<div class="form-group">' +
                    '<label>Select Tag</label>' +
                    '<input type="text" class="form-control" name="select_tag_'+input_num+'">' +
                '</div>' +
            '</div>' +
            '<div class="col-12 col-md-2">' +
               ' <label class="d-md-block d-sm-none d-none">&nbsp;</label>' +
                '<a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a>' +
            '</div>' +
            '<div class="col-12 col-md-5">' +
                '<div class="form-group">' +
                    '<label>Data Type</label>' +
                    '<select name="data_type_'+input_num+'" class="form-control">' +    
                        '<option value="TEXT" selected>Text</option>' +
                        '<option value="VIDEO">Video</option>' +
                        '<option value="IMAGE">Image</option>' +
                    '</select>' +
                '</div>' +
            '</div>' +
        '</div>';
        
        $(".site-info").append(listcontent);
        return false;
    });

    $("#id_newSiteForm").submit(function(event) {
        event.preventDefault();
        $.ajax({ 
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                console.log(response);
                if(response['success']) {
                    alert(response['success']);
                    window.location.href = "../web/";
                }
                if(response['error']) {
                    alert(response['error']);
                    //$("#id_error-text").html("Error: "+response['error']+"");
                }
            },
            error: function (request, status, error) {
                console.log(request.responseText);
            }
        });
    });

    // Edit Site

    $(".siteEdit-info").on('click','.trashEdit', function () {
        $(this).closest('.siteEdit-cont').remove();
        return false;
    });

    $(".add-siteEdit").on('click', function () {
 
        var input_num = parseInt($("#countEdit").text());
        input_num = input_num + 1;
        $("#countEdit").text(''+input_num+'');
        $("input[name='form_numEdit']").val(''+input_num+'');
        var listcontent = '<div class="row form-row siteEdit-cont">' +
            '<div class="col-12 col-md-5">' +
                '<div class="form-group">' +
                    '<label>Data Url</label>' +
                    '<input type="text" class="form-control" name="url_scrapped_'+input_num+'">' +
                '</div>' +
            '</div>' +
            '<div class="col-12 col-md-5">' +
                '<div class="form-group">' +
                    '<label>Select Tag</label>' +
                    '<input type="text" class="form-control" name="select_tag_'+input_num+'">' +
                '</div>' +
            '</div>' +
            '<div class="col-12 col-md-2">' +
               ' <label class="d-md-block d-sm-none d-none">&nbsp;</label>' +
                '<a href="#" class="btn btn-danger trashEdit"><i class="far fa-trash-alt"></i></a>' +
            '</div>' +
            '<div class="col-12 col-md-5">' +
                '<div class="form-group">' +
                    '<label>Data Type</label>' +
                    '<select name="data_type_'+input_num+'" class="form-control">' +    
                        '<option value="TEXT" selected>Text</option>' +
                        '<option value="VIDEO">Video</option>' +
                        '<option value="IMAGE">Image</option>' +
                    '</select>' +
                '</div>' +
            '</div>' +
        '</div>';
        
        $(".siteEdit-info").append(listcontent);
        return false;
    });
    
    $(".editSiteForm").submit(function(event) {
        event.preventDefault();
        $.ajax({ 
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                console.log(response);
                if(response['success']) {
                    alert(response['success']);
                    window.location.href = "../web/";
                }
                if(response['error']) {
                    alert(response['error']);
                    //$("#id_error-text").html("Error: "+response['error']+"");
                }
            },
            error: function (request, status, error) {
                console.log(request.responseText);
            }
        });
    });

    $('.scrapSite').click(function(event){
        event.preventDefault();
        var id = $(this).attr("id");
        var scrap_data = {
            scrapper_id: id
        };
        $.ajax({ 
            data: scrap_data,
            type: 'GET',
            url: $(this).attr('href'),
            success: function(response) {
                console.log(response);
                if(response['success']) {
                    alert(response['success']);
                    window.location.href = "../../web/";
                }
                if(response['error']) {
                    alert(response['error']);
                }
            },
            error: function (request, status, error) {
                console.log(request.response);
            }
        });
        return false;    
    });

    $('.deleteModal').click(function(event){
        event.preventDefault();
        var id = $(this).attr("id");
        var delete_data = {
            delete_id: id
        };
        $.ajax({ 
            data: delete_data,
            type: 'GET',
            url: $(this).attr('href'),
            success: function(response) {
                console.log(response);
                if(response['success']) {
                    alert(response['success']);
                    window.location.href = "../../web/";
                }
                if(response['error']) {
                    alert(response['error']);
                }
            },
            error: function (request, status, error) {
                console.log(request.response);
            }
        });
        return false;    
    });
	
})(jQuery);


$("#table-1").dataTable({
  "columnDefs": [
    { "sortable": false, "targets": [2, 3] }
  ]
});
$("#table-2").dataTable({
  "columnDefs": [
    { "sortable": false, "targets": [0, 2, 3] }
  ],
  order: [[1, "asc"]] //column indexes is zero based

});
$('#save-stage').DataTable({
  "scrollX": true,
  stateSave: true
});
$('.cvs-table').DataTable({
  dom: 'Bfrtip',
  buttons: [
    'copy', 'csv', 'excel', 'pdf', 'print'
  ]
});


