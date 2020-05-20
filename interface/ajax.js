function ajax_call(form_data){

  //for the avoidance of doubt, loop through the provided form data
  //ensure that the value stored in the variable is what we expect
  server_url = "";
  method = "";
  route = "";
  product_location = "";
  server_url = "";
  request_body = "";
  $.each(form_data, function(index, form_data_item) {
    switch(form_data_item['name']){
      case 'url':
        server_url = form_data_item['value'];
        break;
      case 'method':
        method = form_data_item['value'];
        break;
      case 'route':
        route = form_data_item['value'];
        break;
      case 'location':
        product_location = "/"+form_data_item['value'];
        break;
      case 'request_body':
        request_body = form_data_item['value'];
        break;
    }
  });

  //ignore the product_location unless it's needed
  if (route == "/product"){
    complete_url = server_url + route + product_location;
  }
  else {
    complete_url = server_url + route;
  }

  //append the token as a URL param if trying to GET the float
  //workaround for JavaScript ajax method.
  //If working in PostMan, for example, this is not needed
  if( method=="GET" && route=="/float" ){
    request_body_json = $.parseJSON(request_body);
    request_body = "token=" + request_body_json.token;
  }

  //data checked and ready to interact with the server
  return $.ajax({
    method: method,
    url: complete_url,
    contentType: 'application/json',
    dataType: 'json',
    data: request_body,
    success: function(result){
      $('#response_status').html("200");
      $('#response_text').html(JSON.stringify(result,null,4));
      return result;
    },
    error: function (jqXHR, exception) {
      $('#response_status').html(jqXHR.status);
      $('#response_text').html(JSON.stringify(jqXHR.responseJSON,null,4));
      return jqXHR;
    }
  });
}


  

$(document).ready(function() {
  //Collect the form data and 'submit' the form via AJAX
  $('#request_builder').submit(function(event){
    event.preventDefault(); //cancels the form submission
    form_data = $('#request_builder').serializeArray(); //get the form data as an array
    $('#response_status').html(" "); //wipe the contents of the response status
    $('#response_text').html(" "); //wipe the contents of the response text

    if((form_data[2]["name"]=="route" && form_data[2]["value"] == "/product") &&
        (form_data[3]["name"]=="location" && form_data[3]["value"].length==0)) {
          $('#location_feedback').html("The route /product must have a location. Please enter a location");
    }
    else {
      $('#location_feedback').html("");
      ajax_call(form_data); //run the ajax request with the provided details from the form
    }

  });
});