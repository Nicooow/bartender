import {Boisson} from './Boisson.js';

export class Server {
  constructor(bartender) {
    this.Bartender = bartender;
    this.socket = undefined
    console.log("constructeur Server")
  }

  connect() {
    try {
        this.socket = new WebSocket("ws://localhost:12345");
        this.Bartender.Vue.showBarInfo("Connexion au serveur...");
    } catch (exception) {
        console.error(exception);
    }

    this.socket.onerror = () => {
        console.error(error);
        this.Bartender.Vue.showBarInfo("Erreur avec le serveur !");
    };

    this.socket.onclose = () => {
      this.Bartender.Vue.showBarInfo("Connexion avec le serveur perdu...<br>Nouvelle tentative dans 5 secondes");
      setTimeout(()=>{this.connect()}, 5 * 1000) // 5 secondes
    }

    this.socket.onopen = () => {
        this.sendMessage("setupAs|distributeur");
        this.Bartender.Vue.showBarInfo("Connexion réussie !", 1500);
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
      if(args[1] == "boissonAvailable"){
        var boisson = new Boisson(args[2], args[3], args[4], args[5], args[6], args[8]);
        this.Bartender.addAvailableBoisson(boisson);
      }
    }
  }

  askAvailableBoissons(){
    this.Bartender.availableBoissons = [];
    this.sendMessage("ask|availableBoissons");
  }
}
