function changeMode(mode){
  $(".on-sign").addClass("off-sign");
  $(".on-sign").removeClass("on-sign");
  $("#mode"+mode).addClass("on-sign");
}

function changeSelection(){
  console.log("changeSelection")
  $("#selection_alcool, #selection_diluant").toggleClass("selected");
  $("#selection_alcool, #selection_diluant").toggleClass("unselected");
}

function selectAlcool(nom){
  $("#selection_alcool, #selection_diluant").toggleClass("selected");
  $("#selection_alcool, #selection_diluant").toggleClass("unselected");

  $("#selected_alcool .subtitle-off").removeClass("subtitle-off").addClass("subtitle")
  $("#selected_alcool img").attr('src','img/'+nom+'.png');
}

function selectDiluant(nom){
  $("#selection_diluant").removeClass("selected");
  $("#selection_diluant").addClass("unselected");

  $("#selected_diluant .subtitle-off").removeClass("subtitle-off").addClass("subtitle")
  $("#selected_diluant img").attr('src','img/'+nom+'.png');

  setTimeout(function(){
      $("#selected_alcool, #selected_diluant").addClass("ready");
      $("#validate").toggleClass("ready")
  }, 700);
}

function validate(){
  $("#selected_alcool, #selected_diluant").removeClass("ready");
  $("#selected_alcool, #selected_diluant").addClass("hide");
  $("#validate").toggleClass("ready")

  setTimeout(function(){
    $("#progression_text, #progression").toggleClass("ready");
  }, 500);
}

var r=255,g=0,b=0,p=0;

setInterval(function(){
  if(r > 0 && b == 0){
    r--;
    g++;
  }
  if(g > 0 && r == 0){
    g--;
    b++;
  }
  if(b > 0 && g == 0){
    r++;
    b--;
  }
  p += 0.1;
  p = p%5;
  //$("body").get(0).style.setProperty("--color-theme", r+", "+g+", "+b);
  $("#barre").css("width", (p*20)+"%")
  $("#percent_text").html(Math.floor(p*20)+"%")
},200);

function enterScreensaver(){
  $(".sign1").addClass("sign_veille");
  $(".hideScreensaver").addClass("hide");
}

function exitScreensaver(){
  $(".sign1").removeClass("sign_veille");
  $(".hideScreensaver").removeClass("hide");
}

$( document ).ready(function() {
  //enterScreensaver();

  setInterval(function(){
    var i = 0;
    $( ".title_letter" ).each(function() {
      i++;
      setTimeout(function(x, y){
         //$(x).css("transform","translateY(-65px)");
         $(x).css("transform","scale(0.7)");
         //$(x).css("transform","rotate(0.5turn)");
         //$(x).css("transform","translate(-25px, -25px)");
         //$(x).css("opacity",0);
      }, i*200, this, i);
      setTimeout(function(x, y){
         //$(x).css("transform","translateY(0px)");
         $(x).css("transform","none");
         //$(x).css("transform","scale(1)");
         //$(x).css("transform","translate(0px, 0px)");
         $(x).css("opacity",1);
      }, i*200+400, this, i);
    });
  },6000);

});
