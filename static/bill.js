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

  // Please keep this section below in case a future version of jQuery makes
  // jQuery cookie plugin cease functioning:

  // function getCookie(name) {
  //   var cookieValue = null;
  //   if (document.cookie && document.cookie != '') {
  //     var cookies = document.cookie.split(';');
  //     for (var i = 0; i < cookies.length; i++) {
  //       var cookie = $.trim(cookies[i]);
  //       // Does this cookie string begin with the name we want?
  //       if (cookie.substring(0, name.length + 1) == (name + '=')) {
  //         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
  //         break;
  //       }
  //     }
  //   }
  //   return cookieValue;
  // }
  // var csrftoken = getCookie('csrftoken');
  var csrftoken = $.cookie('csrftoken');
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

  // var billarea = new Annotator($(".billarea"));
  var billarea = $(".billarea").annotator();
  var propietary = 'demoUser'
  billarea.annotator('addPlugin', 'Permissions', {
  user: propietary,
  permissions: {
      'read': [propietary],
      'update': [propietary],
      'delete': [propietary],
      'admin': [propietary]
  },
  showViewPermissionsCheckbox: true,
  showEditPermissionsCheckbox: false
  });
  $('.billarea').annotator().annotator('addPlugin', 'AnnotatorViewer');

  billarea.annotator('addPlugin', 'Store', {
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
      'bill_id': window.bill_id,
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

  // FYI: Tags are space-separated, not comma-separated
  // (Learned that from experience)
  billarea.annotator('addPlugin', 'Tags')
};
