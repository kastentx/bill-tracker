// var selected;

window.onload = function() {
  // $("span").each(function() {
  //   $(this).click(function() {
  //     if (selected) {
  //       $(selected).toggleClass("selected-sentence");
  //       $(this).toggleClass("selected-sentence");
  //       selected = this;
  //     } else {
  //       $(this).toggleClass("selected-sentence");
  //       selected = this;
  //     }
  //   });
  // });

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

  var annotator = new Annotator($(".billarea"));

  annotator.addPlugin('Store', {
    // The endpoint of the store on your server.
    prefix: '/annotations',

    urls: {
      // These are the default URLs.
      create:  '/',
      read:    '/:id',
      update:  '/:id',
      destroy: '/:id',
      search:  '/search'
    },

    // Attach the uri of the current page to all annotations to allow search.
    annotationData: {
      // 'uri': 'http://this/document/only',
    },

    // // This will perform a "search" action when the plugin loads. Will
    // // request the last 20 annotations for the current url.
    // // eg. /store/endpoint/search?limit=20&uri=http://this/document/only
    // loadFromSearch: {
    //   'limit': 20,
    //   'uri': 'http://this/document/only'
    // }
  });

  annotator.addPlugin('Tags')
};
