$.get('http://localhost:8000/getbill/',
  { number: 10 },
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
