document.addEventListener('DOMContentLoaded', function() {

  var insertButton = document.getElementById('button-insert');
  var insertedContainer = document.getElementById('inserted-container');

  insertButton.onclick = function() {
    insertedContainer.style.animationName = "animationIn";
    insertedContainer.style.animationDuration = "0.4s";

    window.setTimeout(function() {
      insertedContainer.style.animationName = "";
    }, 2000);
  }
});
