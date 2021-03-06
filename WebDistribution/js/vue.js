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
  }

  setEventsBoissons(){
    $( ".itemBoisson" ).click((event) => {this.Controller.onBoissonClick(event)});
  }

  updateLevelMode(level){
    $(".on-sign").addClass("off-sign");
    $(".on-sign").removeClass("on-sign");
    $("#mode"+level).addClass("on-sign");
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

  hideBarInfo(){
    clearTimeout(this.timeoutBarInfo);
    $("#page").removeClass("blur");
    $("#barInfoBackground").addClass("hide");
    $("#barInfo .subtitle").html("");
  }

  showSelectionAlcool(){
    this.hideSelections();
    $("#selection_alcool").removeClass("unselected");
    $("#selection_alcool").addClass("selected");
  }

  showSelectionDiluant(){
    this.hideSelections();
    $("#selection_diluant").removeClass("unselected");
    $("#selection_diluant").addClass("selected")
  }

  hideSelections(){
    $("#selection_alcool").removeClass("selected");
    $("#selection_alcool").addClass("unselected");
    $("#selection_diluant").removeClass("selected");
    $("#selection_diluant").addClass("unselected");
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

  setSelectedBoisson(boisson){
    var cat = parseFloat(boisson.pourcentageAlcool)>0 ? "#selected_alcool" : "#selected_diluant";
    if(boisson == undefined){
      $(cat+" .subSelected").addClass("subtitle-off").removeClass("subtitle");
      $(cat+" img").attr("src", "img/no.png");
    }else{
      $(cat+" .subSelected").addClass("subtitle").removeClass("subtitle-off");
      $(cat+" img").attr("src", boisson.logo);
    }
  }
}
