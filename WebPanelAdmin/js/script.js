var socket = null;
var pageActuel = "";

function switchMode(){
  if($(".bootstrap-dark").length){
    $(".bootstrap-dark").addClass("bootstrap").removeClass("bootstrap-dark");
  }else{
    $(".bootstrap").addClass("bootstrap-dark").removeClass("bootstrap");
  }

  if ($(window).width() <= 800) {
    $('.navbar-toggler:not(.collapsed)').click();
  }
}

function switchModeEtat(jour){
  if($(".bootstrap-dark").length && jour){
    $(".bootstrap-dark").addClass("bootstrap").removeClass("bootstrap-dark");
  }else if($(".bootstrap").length && !jour){
    $(".bootstrap").addClass("bootstrap-dark").removeClass("bootstrap");
  }

  if ($(window).width() <= 800) {
    $('.navbar-toggler:not(.collapsed)').click();
  }
}

function erreur(type, texte){
  $("#errors").append('<div class="alert alert-'+type+' alert-dismissible fade show" role="alert"><strong>Erreur :</strong> '+texte+'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>')
}

function connexionServeur(){
  $("#connexion").show();

  try {
      socket = new WebSocket("ws://192.168.1.73:12345");
  } catch (exception) {
      console.error(exception);
      erreur("danger", "impossible de se connecter au serveur ("+exception+")");
      $("#navbarSupportedContent .nav-item.active").removeClass("active");
      $("#connexion").hide();
  }

  socket.onerror = function(error) {
      console.error(error);
      erreur("danger", "impossible de se connecter au serveur");
      $("#navbarSupportedContent .nav-item.active").removeClass("active");
      $("#connexion").hide();
  };

  socket.onopen = function(event) {
      $("#connexion").hide();
      $("#page").show();

      this.onclose = function(event) {
          $("#page").hide()
          $("#navbarSupportedContent .nav-item.active").removeClass("active");
          erreur("danger", "connexion avec le serveur coupée, veuillez recharger la page.");
      };

      this.onmessage = function(event) {
          parseMessage(event.data);
      };
  };
}

function sendMessage(message){
  socket.send(message);
}

function parseMessage(message){
  args = message.split("|");
  fnct = args[0];
  console.log(args);
  if(fnct == "page"){
    setPage(args[1]);
  }else if(fnct == "addElement"){
    if(args[1] == "cuve"){
      addCuve(args[2], args[3], args[4], args[5]);
    }else if(args[1] == "boisson"){
      addBoissons(args[2], args[3], args[4], args[5]);
    }
  }else if(fnct == "animation"){
    if(args[1] == "cuves"){
      setTimeout(function(){
        $("#listCuves").animate({scrollLeft: 200}, 2000);
        $("#listCuves").animate({scrollLeft: 0}, 1000);
      }, 500);
    }
  }else if(fnct == "update"){
    if(args[1] == "cuve"){
       if(pageActuel == "accueil"){
         $("#cuve-"+args[2]+"-name").html(args[3])
         $("#cuve-"+args[2]+"-color").css("fill", args[4])
         $("#cuve-"+args[2]+"-level").css("transform", "translate(0,"+args[5]+"px)")
       }
    }
  }
}

function setPage(page){
  pageActuel = page;
  $("#navbarSupportedContent .nav-item.active").removeClass("active");
  $("#navbarSupportedContent .btn-"+page).addClass("active")
  if(page=="accueil"){
    $("#page").html(`<h1>Accueil</h1> <h5>Etat des cuves en direct</h5>
                     <div class="container testimonial-group d-flex justify-content-center">
                      <div class="row" id="listCuves">
                      </div>
                     </div><br><h5>Autres informations</h5>`);
    sendMessage("ask|cuves");
  }else if(page=="listBoissons"){
    $("#page").html(`<h1>Liste des boissons</h1> <button type="button" onclick="setPage('newBoisson')" style="margin-bottom: 10px;" class="align-self-center btn btn-outline-info btn-block">Nouvelle boisson</button> <div class="row row-cols-1 row-cols-sm-1 row-cols-md-2 row-cols-lg-2 row-cols-xl-3" id="listBoissons"> </div>`);
    sendMessage("ask|boissons");
  }else if(page=="newBoisson"){
    $("#page").html(`
      <h2>Nouvelle boisson</h2>
      <div class="jumbotron mx-auto" style="max-width: 600px;">
      <form>
        <div class="form-group">
          <label for="nomAffichage">Nom complet</label>
          <input type="text" class="form-control" id="nomAffichage" placeholder="Nom d'affichage complet">
        </div>
        <div class="form-group">
          <label for="nomCourt">Nom court</label>
          <input type="text" class="form-control" id="nomCourt" placeholder="Sans espace">
        </div>
        <div class="form-group">
          <label for="nomCourt">Couleur de la boisson</label>
          <input type="color" class="form-control" id="couleur">
        </div>
        <div class="form-group">
          <label for="nomCourt">Pourcentage d'alcool de la boisson</label>
          <input type="number" class="form-control" id="pourcentageAlcool" placeholder="0 si non alcoolisé, séparé par un .">
        </div>
        <div class="form-group">
          <label for="nomCourt">Logo de la boisson (.png)</label>
          <input type="file" class="form-control" accept="image/png" id="logo">
        </div>
        <button type="submit" class="btn btn-primary btn-block">Créer</button>
      </form>
      </div>
      `);
  }
  if ($(window).width() <= 800) {
    $('.navbar-toggler:not(.collapsed)').click();
  }
}

function addCuve(num, name, color, level){
  $("#listCuves").append(`
    <div class="col-xs-4">
      <div class="card text-center" style="width: 7rem;">
        <div class="card-body">
          <h5 class="card-title">Cuve ${num}</h5>
          <p class="card-text" id="cuve-${num}-name">${name}</p>
          <div class="d-flex justify-content-center">
            <div class="banner">
              <div class="fill" id="cuve-${num}-level" style="transform: translate(0, 250px);">
                <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="300px" height="300px" viewBox="0 0 300 300" enable-background="new 0 0 300 300" xml:space="preserve">
                  <path id="cuve-${num}-color" class="waveShape" style="fill: ${color};" d="M300,300V2.5c0,0-0.6-0.1-1.1-0.1c0,0-25.5-2.3-40.5-2.4c-15,0-40.6,2.4-40.6,2.4
              c-12.3,1.1-30.3,1.8-31.9,1.9c-2-0.1-19.7-0.8-32-1.9c0,0-25.8-2.3-40.8-2.4c-15,0-40.8,2.4-40.8,2.4c-12.3,1.1-30.4,1.8-32,1.9
              c-2-0.1-20-0.8-32.2-1.9c0,0-3.1-0.3-8.1-0.7V300H300z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    `);
    $("#cuve-"+num+"-level").css("transform", "translate(0,250px)")
    setTimeout(function(){
      $("#cuve-"+num+"-level").css("transform", "translate(0,"+level+"px)")
    }, 10);

}

function addBoissons(name, short_name, color, levelAlcool){
  $("#listBoissons").append(`
    <div class="col">
      <div class="media">
        <img style="height:70px; width:70px;" src="${short_name}" class="align-self-center mr-3">
        <div class="media-body align-self-center">
          <div class="row">
            <div class="col">
              <h5 class="mt-0">${name}</h5>
              `+ ((levelAlcool=="0") ? "" : levelAlcool + "° d'alcool") + `
              </div>
            <div class="col align-self-center text-right">
              <button type="button" class="btn btn-secondary">Modifier</button>
            </div>
          </div>
          </div>
      </div>
    </div>
    `);
}

$( document ).ready(function() {
  $("#connexion").show();
  setTimeout(function(){
    connexionServeur();
  }, 500);

});
