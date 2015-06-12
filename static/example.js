// using jQuery
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = $.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// console.log(csrftoken);

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$.post('http://localhost:8000/addbill/',
  { number: 10, format: 'json' },
  function(data) {
    data = $.parseJSON(data)[0]
    console.log(data);
    bill = $('#bill');
    bill_append(data);
  });

var bill_append = function(data) {
  for (key in data) {
    if (typeof data[key] === "object") {
      bill_append(data[key]);
    } else {
      bill.append("<p>" + key + ": " + data[key] + "</p>");
    }
  }
};
