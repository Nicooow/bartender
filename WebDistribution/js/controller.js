export class Controller {
  constructor(bartender) {
    this.Bartender = bartender;
    console.log("constructeur Controller");
  }

  onModeLevelChange(event){
    var level = $(event.target).data("modelevel");
    this.Bartender.setLevelMode(parseInt(level));
  }

  onBodyClick(event){
    if(this.Bartender.screensaverEnabled){
      this.Bartender.setScreensaver(false);
    }else{
      this.Bartender.clearTimeoutScreensaver();
      this.Bartender.startTimeoutScreensaver();
    }
  }

  onBoissonClick(event){
    var id = $(event.target).parent(".itemBoisson").data("id");
    this.Bartender.boissonClicked(id);
  }

  onSelectedAlcoolClick(event){
    this.Bartender.Vue.showSelectionAlcool();
  }

  onSelectedDiluantClick(event){
    this.Bartender.Vue.showSelectionDiluant();
  }

  onValidateClick(event){
    this.Bartender.sendChoices();
  }

  onCancelClick(event){
    
  }
}
