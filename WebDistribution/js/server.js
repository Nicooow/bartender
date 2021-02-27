export class Server {
  constructor() {
    this.socket = undefined
    console.log("constructeur Server")
  }

  connect() {
    try {
        this.socket = new WebSocket("ws://192.168.3.34:12345");
    } catch (exception) {
        console.error(exception);
        erreur("danger", "impossible de se connecter au serveur ("+exception+")");
        $("#navbarSupportedContent .nav-item.active").removeClass("active");
        $("#connexion").hide();
    }

    this.socket.onerror = function(error) {
        console.error(error);
    };

    this.socket.onopen = function(event) {
        console.log("onopen")
    };
  }
}
