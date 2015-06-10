var selected;

window.onload = function() {
  $("span").each(function() {
    $(this).click(function() {
      if (selected) {
        $(selected).toggleClass("selected-sentence");
        $(this).toggleClass("selected-sentence");
        selected = this;
      } else {
        $(this).toggleClass("selected-sentence");
        selected = this;
      }
    });
  });
};
