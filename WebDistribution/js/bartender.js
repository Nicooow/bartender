import {Server} from './server.js';
import {Vue} from './vue.js';
import {Controller} from './controller.js';
import {Boisson} from './Boisson.js';

export default class Bartender {
  constructor(){
    console.log("constructeur")
    this.Server = new Server(this);
    this.Controller = new Controller(this);
    this.Vue = new Vue(this);

    // VARS
    this.availableBoissons = [];
    this.selectedAlcool = undefined;
    this.selectedDiluant = undefined;

    // INITIALISATION
    this.setLevelMode(2);
    this.startTimeoutScreensaver();
    //this.setScreensaver(true)
    this.Server.connect();
  }

  setLevelMode(level){
    this.levelMode = level;
    this.Vue.updateLevelMode(level);
  }

  setScreensaver(enable){
    if(enable && !this.screensaverEnabled){
      this.screensaverEnabled = true;
      this.Vue.enterScreensaver();
    }else if(enable == false){
      this.screensaverEnabled = false;
      this.Vue.exitScreensaver();
    }
  }

  clearTimeoutScreensaver(){
    clearTimeout(this.timeoutScreensaver);
  }

  startTimeoutScreensaver(){
    this.timeoutScreensaver = window.setTimeout(() => {this.setScreensaver(true)}, 5 * 60 * 1000); // 5 minutes
  }

  resetBoissonsData(){
    this.selectedDiluant = undefined;
    this.selectedAlcool = undefined;
    this.availableBoissons = [];
  }

  addAvailableBoisson(boisson){
    this.availableBoissons[parseInt(boisson.id)] = boisson;
  }

  availableBoissonsReceived(){
    this.Vue.resetBoissons();
    this.Vue.showSelectionAlcool();
    for(b in this.availableBoissons){
      this.Vue.addBoisson(this.availableBoissons[b]);
    }
    this.Vue.setEventsBoissons();
  }

  boissonClicked(id){
    if(parseInt(id) in this.availableBoissons){
      var boisson = this.availableBoissons[parseInt(id)];
      if(parseFloat(boisson.pourcentageAlcool)>0){
        this.selectedAlcool = boisson;
        this.Vue.showSelectionDiluant();
      }else{
        this.selectedDiluant = boisson;
      }
      this.Vue.setSelectedBoisson(boisson);
    }
  }
}


setTimeout(function(){
    $("#selected_alcool, #selected_diluant").addClass("ready");
    $("#validate").toggleClass("ready")
}, 1000000);

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
  $("body").get(0).style.setProperty("--color-theme", r+", "+g+", "+b);
  $("#barre").css("width", (p*20)+"%")
  $("#percent_text").html(Math.floor(p*20)+"%")
},20);

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
