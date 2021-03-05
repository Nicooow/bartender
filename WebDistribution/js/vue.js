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
}
