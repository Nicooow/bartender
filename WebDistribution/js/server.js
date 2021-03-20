import {Boisson} from './boisson.js';

export class Server {
  constructor(bartender) {
    this.Bartender = bartender;
    this.socket = undefined
    console.log("constructeur Server")
  }

  connect() {
    try {
        this.socket = new WebSocket("ws://192.168.3.29:12345");
        this.Bartender.Vue.showBarInfo("Connexion au serveur...");
    } catch (exception) {
        console.error(exception);
    }

    this.socket.onerror = (error) => {
        console.error(error);
        this.Bartender.Vue.showBarInfo("Erreur avec le serveur !");
    };

    this.socket.onclose = () => {
      this.Bartender.Vue.showBarInfo("Connexion avec le serveur perdu...<br>Nouvelle tentative dans 5 secondes");
      setTimeout(()=>{this.connect()}, 5 * 1000) // 5 secondes
    }

    this.socket.onopen = () => {
        this.sendMessage("setupAs|distributeur");
        this.Bartender.Vue.showBarInfo("Connexion réussie !", 1000);
        this.Bartender.Vue.setSelectedBoisson(-1);
        this.Bartender.Vue.setSelectedBoisson(-2);
        this.askAvailableBoissons();

        this.socket.onmessage = () => {
            this.parseMessage(event.data);
        };
    };
  }

  sendMessage(message){
    this.socket.send(message);
  }

  parseMessage(message){
    var args = message.split("|");
    var fnct = args[0];
    console.log(args);

    if(fnct == "addElement"){
      if(args[1] == "availableBoissons"){
        var boisson = new Boisson(args[2], args[3], args[4], args[5], args[6], args[8]);
        this.Bartender.addAvailableBoisson(boisson);
      }
    }else if(fnct == "askOk"){
      if(args[1] == "availableBoissons"){
        this.Bartender.availableBoissonsReceived();
      }
    }else if(fnct == "themeColor"){
      this.Bartender.Vue.setThemeColor(args[1]);
    }else if(fnct == "distribution"){
      if(args[1] == "start"){
        this.Bartender.Vue.showProgressBar();
      }else if(args[1] == "stop"){
        this.Bartender.Vue.hideProgressBar();
        setTimeout(()=>{
          this.Bartender.Vue.setSelectedBoisson(-1);
          this.Bartender.Vue.setSelectedBoisson(-2);
          this.Bartender.Vue.showSelectionAlcool();
          this.Bartender.Vue.setPercent(0);
        }, 500);
      }
    }else if(fnct == "percentDistribution"){
      this.Bartender.Vue.setPercent(args[1]);
    }
  }

  askAvailableBoissons(){
    this.Bartender.resetBoissonsData();
    this.sendMessage("ask|availableBoissons");
  }
}
