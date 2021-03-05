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
    };
  }

  sendMessage(message){
    this.socket.send(message);
  }
}
