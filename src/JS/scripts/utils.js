var settings = {
    "method": "GET",
    "headers": {
      "Authorization": `Bearer ${BEARER_TOKEN}`,
    },
  };

  function doGet(url, callback, errorHandle) {
      settings["url"] = url;
      $.ajax(settings).done(function (response) {
          callback(response);
      }).fail(function(err) {
        if (errorHandle !== null) {
          errorHandle(err);
        }
      });
  } 