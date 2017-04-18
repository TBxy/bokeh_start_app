
(function($, window) {

console.log("changed")

}).call(this, jQuery, window);


(function($){
  $(function(){


    log.setDefaultLevel('trace') // set log level to trace


    log.debug("side nav init")
    $('.button-collapse').sideNav();
    $('.modal').modal();
  }); // end of document ready
})(jQuery); // end of jQuery name space

jQuery(document).ready(function() {
  checkContainer();
});

function checkContainer () {
  if($('.bk-canvas-events').is(':visible')){ //if the container is visible on the page
   log.info("bokeh plot loaded") 
    //$("#bokeh-plot1").show()
    $("#mybk-loader").hide(2)
  } else {
    log.trace("bokeh plot loading ...") 
    //$("#bokeh-plot1").hide(1)
    setTimeout(checkContainer, 100); //wait 50 ms, then try again
  }
}
