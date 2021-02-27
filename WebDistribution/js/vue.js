export class Vue {
  constructor(bartender) {
    this.Bartender = bartender;
    this.Controller = this.Bartender.Controller;
    console.log("constructeur Vue");

    this.setEvents();
  }

  setEvents(){
    $( "#modesList span" ).click((event) => {this.Controller.onModeLevelChange(event)});
    $( "body" ).click((event) => {this.Controller.onBodyClick(event)});
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
}
