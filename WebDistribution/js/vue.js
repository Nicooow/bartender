export class Vue {
  constructor(bartender) {
    this.Bartender = bartender;
    this.Controller = this.Bartender.Controller;
    console.log("constructeur Vue");

    this.setEvents();
    this.timeoutBarInfo = undefined;
  }

  setEvents(){
    $( "#modesList span" ).click((event) => {this.Controller.onModeLevelChange(event)});
    $( "body" ).click((event) => {this.Controller.onBodyClick(event)});
    $( "#selected_alcool img" ).click(() => {this.Controller.onSelectedAlcoolClick(event)});
    $( "#selected_diluant img" ).click(() => {this.Controller.onSelectedDiluantClick(event)});
    $( "#selected_alcool h1" ).click(() => {this.Controller.onSelectedAlcoolClick(event)});
    $( "#selected_diluant h1" ).click(() => {this.Controller.onSelectedDiluantClick(event)});
    $( "#validate" ).click(() => {this.Controller.onValidateClick(event)});
    $( "#cancel").click(() => {this.Controller.onCancelClick(event)});
    $( "#ethylotestBtn").click(() => {this.Controller.onEthylotestClick(event)});
    $( "#pageEthylotest #container").click(() => {this.Controller.onCloseEthylotestClick(event)});
  }

  setEventsBoissons(){
    $( ".itemBoisson" ).click((event) => {this.Controller.onBoissonClick(event)});
  }

  updateLevelMode(level){
    $(".on-sign").addClass("off-sign");
    $(".on-sign").removeClass("on-sign");
    $("#mode"+level).addClass("on-sign");
    $("#mode"+level).removeClass("off-sign");
  }

  enterScreensaver(){
    $(".sign1").addClass("sign_veille");
    $(".hideScreensaver").addClass("totalHide");
  }

  exitScreensaver(){
    $(".sign1").removeClass("sign_veille");
    $(".hideScreensaver").removeClass("totalHide");
  }

  showBarInfo(message, timer = -1){
    clearTimeout(this.timeoutBarInfo);

    $("#page").addClass("blur");
    $("#barInfoBackground").removeClass("hide");
    $("#barInfo .subtitle").html(message);

    if(timer != -1){
      this.timeoutBarInfo = setTimeout(()=>{this.hideBarInfo()}, timer);
    }
  }

  resetScreen(){
    this.hidePreValidate();
    this.hideSelections();
    this.hideProgressBar();
    this.hideSelected();
  }

  hideBarInfo(){
    clearTimeout(this.timeoutBarInfo);
    $("#page").removeClass("blur");
    $("#barInfoBackground").addClass("hide");
    $("#barInfo .subtitle").html("");
  }

  showSelectionAlcool(){
    this.resetScreen()
    this.showSelected();
    $("#selection_alcool").removeClass("unselected");
    $("#selection_alcool").addClass("selected");
    clearTimeout(this.Bartender.timeoutPreValidate);
  }

  showSelectionDiluant(){
    this.resetScreen()
    this.showSelected();
    $("#selection_diluant").removeClass("unselected");
    $("#selection_diluant").addClass("selected")
  }

  hideSelections(){
    $("#selection_alcool").removeClass("selected");
    $("#selection_alcool").addClass("unselected");
    $("#selection_diluant").removeClass("selected");
    $("#selection_diluant").addClass("unselected");
  }

  showSelected(){
    $("#selected_alcool, #selected_diluant").removeClass("hide");
  }

  hideSelected(){
    $("#selected_alcool, #selected_diluant").addClass("hide");
  }

  resetBoissons(){
    $("#list_alcool").html("");
    $("#list_diluant").html("");
  }

  addBoisson(boisson){
    var cat = parseFloat(boisson.pourcentageAlcool)>0 ? "#list_alcool" : "#list_diluant";
    var html = `<div class="itemBoisson" id="boisson_${boisson.id}" data-id="${boisson.id}"><img src="${boisson.logo}" /></div>`;
    $(cat).append(html);
  }

  addNoBoisson(){
    var html = `<div class="itemBoisson" id="boisson_-1" data-id="-1"><img src="img/no.png"></div>`;
    $("#list_alcool").append(html);
    html = `<div class="itemBoisson" id="boisson_-2" data-id="-2"><img src="img/no.png"></div>`;
    $("#list_diluant").append(html);
  }

  setSelectedBoisson(id){
    if(id==-1){
      $("#selected_alcool .subSelected").addClass("subtitle-off").removeClass("subtitle");
      $("#selected_alcool img").attr("src", "img/no.png");
    }else if(id==-2){
      $("#selected_diluant .subSelected").addClass("subtitle-off").removeClass("subtitle");
      $("#selected_diluant img").attr("src", "img/no.png");
    }else{
      var boisson = this.Bartender.availableBoissons[parseInt(id)];
      var cat = parseFloat(boisson.pourcentageAlcool)>0 ? "#selected_alcool" : "#selected_diluant";
      $(cat+" .subSelected").addClass("subtitle").removeClass("subtitle-off");
      $(cat+" img").attr("src", boisson.logo);
    }
  }

  showPreValidate(){
    this.hideSelections();
    $("#selected_alcool").addClass("ready");
    $("#selected_diluant").addClass("ready");
    $("#validate").addClass("ready");
  }

  hidePreValidate(){
    $("#selected_alcool").removeClass("ready");
    $("#selected_diluant").removeClass("ready");
    $("#validate").removeClass("ready");
  }

  setThemeColor(color){
    var hex = parseInt(color.slice(1), 16);
    var r = (hex >> 16) & 255;
    var g = (hex >> 8) & 255;
    var b = hex & 255;

    $("body").get(0).style.setProperty("--color-theme", r+", "+g+", "+b);
  }

  showProgressBar(){
    this.resetScreen();
    setTimeout(function(){
      $("#progression_text, #progression").addClass("ready");
    }, 250);
  }

  hideProgressBar(){
    $("#progression_text, #progression").removeClass("ready");
  }

  setPercent(percent){
    setTimeout(function(){
      $("#barre").css("width", (percent)+"%")
      $("#percent_text").html(Math.floor(percent)+"%")
    }, 1);
  }

  showEthylotest(){
    $("#pageEthylotest").removeClass("hide");
    $("#page").addClass("blur");
  }

  hideEthylotest(){
    $("#pageEthylotest").addClass("hide");
    $("#page").removeClass("blur");
  }

  updateEthylotest(value){
    $("#pageEthylotest #valueEthylotest").html(value);
  }
}
