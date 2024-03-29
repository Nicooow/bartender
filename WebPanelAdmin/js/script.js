var socket = null;
var pageActuel = "";
var pageActuelId = -1;

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
  if(type=="info"){
    $("#errors").append('<div class="alert alert-'+type+' alert-dismissible fade show" role="alert"><strong>Info :</strong> '+texte+'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>')
  }else{
    $("#errors").append('<div class="alert alert-'+type+' alert-dismissible fade show" role="alert"><strong>Erreur :</strong> '+texte+'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>')
  }
}

function connexionServeur(){
  $("#errors").html("");
  $("#connexion").show();
  $("#btnReload").hide();

  try {
      socket = new WebSocket("ws://bartender.local:12345");
  } catch (exception) {
      console.error(exception);
      erreur("danger", "impossible de se connecter au serveur ("+exception+")");
      $("#btnReload").show();
      $("#navbarSupportedContent .nav-item.active").removeClass("active");
      $("#connexion").hide();
  }

  socket.onerror = function(error) {
      console.error(error);
      erreur("danger", "impossible de se connecter au serveur.");
      $("#navbarSupportedContent .nav-item.active").removeClass("active");
      $("#connexion").hide();
      $("#btnReload").show();
  };

  socket.onopen = function(event) {
      $("#connexion").hide();
      $("#btnReload").hide();
      $("#page").show();
      setPage("accueil")

      this.onclose = function(event) {
          $("#page").hide()
          $("#navbarSupportedContent .nav-item.active").removeClass("active");
          erreur("danger", "connexion avec le serveur coupée, veuillez recharger la page.");
          $("#btnReload").show();
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
      if(pageActuel=="accueil"){
         addCuveAccueil(args[2], args[11], args[12], args[5], args[14], args[15]);
      }else if(pageActuel=="listCuves"){
         addCuve(args[2], args[3], args[4], args[5],  args[6], args[7], args[8], args[9], args[10], args[11], args[12], args[13], args[14], args[15]);
      }
    }else if(args[1] == "boisson"){
      if(pageActuel=="modifyCuve" || pageActuel=="newCuve"){
        addBoissonSelect(args[2], args[3], args[4], args[5],  args[6], args[7], args[8]);
      }else{
        addBoisson(args[2], args[3], args[4], args[5],  args[6], args[7], args[8]);
      }
    }else if(args[1] == "reglages"){
      addReglages(args[2], args[3], args[4]);
    }else if(args[1] == "reglage"){
      addReglage(args[2], args[3], args[4], args[5],  args[6], args[7]);
    }
  }else if(fnct == "animation"){
    if(args[1] == "cuves"){
      setTimeout(function(){
        $("#listCuves").animate({scrollLeft: 200}, 2000);
        $("#listCuves").animate({scrollLeft: 0}, 1000);
      }, 500);
    }
  }else if(fnct == "updateElement"){
    if(args[2] == "cuve"){ // quantite3, quantiteMax4, niveau5, pompePinId6, dmPinId7, debitmetreMlParTick8, bId, bNomAffiche, bNomCourt, bCouleur
       idToUpdate = args[1]

       $("#cuve-"+idToUpdate+"-name").html(args[11])
       $("#cuve-"+idToUpdate+"-color").css("fill", args[12])
       $("#cuve-"+idToUpdate+"-level").css("transform", "translate(0,"+args[5]+"px)")

       $("#cuve_"+ idToUpdate +" #text_quantite_cuve").html(args[3])
       $("#cuve_"+ idToUpdate +" #text_quantiteMax_cuve").html(args[4])
       $("#cuve_"+ idToUpdate +" #text_pompePinId_cuve").html(args[6])
       $("#cuve_"+ idToUpdate +" #text_dmPinId_cuve").html(args[7])
       $("#cuve_"+ idToUpdate +" #text_debitmetreMlParTick_cuve").html(args[8])

       $("#data_cuve_" + idToUpdate + " #quantite").val(args[3])
       $("#data_cuve_" + idToUpdate + " #quantiteMax").val(args[4])
       $("#data_cuve_" + idToUpdate + " #niveau").val(args[5])
       $("#data_cuve_" + idToUpdate + " #pompePinId").val(args[6])
       $("#data_cuve_" + idToUpdate + " #dmPinId").val(args[7])
       $("#data_cuve_" + idToUpdate + " #debitmetreMlParTick").val(args[8])
       $("#data_cuve_" + idToUpdate + " #bId").val(args[9])
       $("#data_cuve_" + idToUpdate + " #bNomAffiche").val(args[10])
       $("#data_cuve_" + idToUpdate + " #bNomCourt").val(args[11])
       $("#data_cuve_" + idToUpdate + " #bCouleur").val(args[12])

       $("#cuve_"+ idToUpdate +" #button_700_cuve").prop("disabled",parseInt(args[3])+700>parseInt(args[4]));
       $("#cuve_"+ idToUpdate +" #button_750_cuve").prop("disabled",parseInt(args[3])+750>parseInt(args[4]));
       $("#cuve_"+ idToUpdate +" #button_1000_cuve").prop("disabled",parseInt(args[3])+1000>parseInt(args[4]));
       $("#cuve_"+ idToUpdate +" #button_1500_cuve").prop("disabled",parseInt(args[3])+1500>parseInt(args[4]));
       $("#cuve_"+ idToUpdate +" #button_2000_cuve").prop("disabled",parseInt(args[3])+2000>parseInt(args[4]));
       $("#cuve_"+ idToUpdate +" #button_more_cuve").prop("disabled",parseInt(args[3])>=parseInt(args[4]));

       $("#cuve_"+ idToUpdate +" .glowingDiv").toggleClass("glowing", Boolean(parseInt(args[13])))
       $("#cuve_"+ idToUpdate +" .pompe-on").toggleClass("disabled", Boolean(parseInt(args[13])))
       $("#cuve_"+ idToUpdate +" .pompe-off").toggleClass("disabled", !Boolean(parseInt(args[13])))

    }else if(args[2] == "boisson"){
      idToUpdate = args[1]

      $("#data_boisson_" + idToUpdate + " #nomCourt").val(args[4])
      $("#data_boisson_" + idToUpdate + " #nomAffichage").val(args[3])
      $("#data_boisson_" + idToUpdate + " #couleur").val(args[5])
      $("#data_boisson_" + idToUpdate + " #pourcentageAlcool").val(args[6])
      $("#data_boisson_" + idToUpdate + " #logo").val(args[7])

      $("#boisson_"+ idToUpdate +" #nomAffichage_boisson").html(args[3])
      $("#boisson_"+ idToUpdate +" #text_alcool_boisson").html(parseInt(args[6])==0 ? "" : args[6] + "° d'alcool")
      $("#boisson_"+ idToUpdate +" #logo_boisson").attr("src",args[7])
    }
  }else if(fnct == "deleteElement"){
    if(args[1] == "cuve"){
      idToDelete = args[2];
      $("#cuve_"+idToDelete).remove()
    }
    else if(args[1] == "boisson"){
    idToDelete = args[2];
    $("#boisson_"+idToDelete).remove()
    }
  }else if(fnct == "editingElement"){
    if(args[1] == "cuve"){
      idEditing = args[2];
      isEditing = Boolean(parseInt(args[3]))
      toggleCantEditCuve(idEditing, isEditing)
    }else if(args[1] == "boisson"){
      idEditing = args[2];
      isEditing = Boolean(parseInt(args[3]))
      toggleCantEditBoisson(idEditing, isEditing)
    }
  }else if(fnct == "toggleElement"){
    if(args[1] == "cuve"){
      idToggle = args[2]
      toggle = Boolean(parseInt(args[3]))

      if(toggle){
        $("#cuve_" + idToggle + " .btn-toggle-cuve").removeClass("btn-success");
        $("#cuve_" + idToggle + " .btn-toggle-cuve").addClass("btn-warning");
        $("#cuve_" + idToggle + " .btn-toggle-cuve").html("Désactiver");
        $("#cuve_" + idToggle + " .btn-toggle-cuve").attr("onclick",`toggleCuve(${idToggle}, 0)`);
        $(".tinyCuve#cuve_" + idToggle).removeClass("blur")
      }else{
        $("#cuve_" + idToggle + " .btn-toggle-cuve").addClass("btn-success");
        $("#cuve_" + idToggle + " .btn-toggle-cuve").removeClass("btn-warning");
        $("#cuve_" + idToggle + " .btn-toggle-cuve").html("Activer");
        $("#cuve_" + idToggle + " .btn-toggle-cuve").attr("onclick",`toggleCuve(${idToggle}, 1)`);
        $(".tinyCuve#cuve_" + idToggle).addClass("blur")
      }
    }
  }else if(fnct == "error"){
    erreur(args[1], args[2])
  }
}

function setPage(page, arg1){
  if(pageActuel=="modifyBoisson"){
    sendMessage("editing|boisson|" + pageActuelId + "|0");
  }else if(pageActuel=="modifyCuve"){
      sendMessage("editing|cuve|" + pageActuelId + "|0");
  }

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
    $("#page").html(`<h1>Liste des boissons</h1>
      <div class="d-flex w-100" role="group">
        <button type="button" onclick="setPage('newBoisson')" style="width:auto; margin-bottom: 10px; margin-right:10px;" class="w-100 align-self-center btn btn-outline-info">Nouvelle boisson</button>
        <button type="button" onclick="toggleSuppressionBoisson()" style="margin-bottom: 10px;" class="align-self-center btn btn-outline-danger" id="toggleSuppressionBoisson"><i class="bi-trash-fill"></i></button>
      </div>
      <div class="row row-cols-1 row-cols-sm-1 row-cols-md-2 row-cols-lg-2 row-cols-xl-3" id="listBoissons"> </div>
    `);
    sendMessage("ask|boissons");
  }else if(page=="newBoisson"){
    showBoissonModele(true, 0, "", "", "#000", "", "")
  }else if(page=="modifyBoisson"){
    modifyBoisson(`#data_boisson_${arg1}`)
    pageActuelId = arg1
  }else if(page=="newCuve"){
    showCuveModele(true, 0, 0, 0, 0, 0, 0, -1)
  }else if(page=="modifyCuve"){
    modifyCuve(`#data_cuve_${arg1}`)
    pageActuelId = arg1
  }else if(page=="listCuves"){
    $("#page").html(`<h1>Liste des cuves</h1>
      <div class="d-flex w-100" role="group">
        <button type="button" onclick="setPage('newCuve')" style="width:auto; margin-bottom: 10px; margin-right:10px;" class="w-100 align-self-center btn btn-outline-info">Nouvelle cuve</button>
        <button type="button" onclick="toggleSuppressionCuve()" style="margin-bottom: 10px;" class="align-self-center btn btn-outline-danger" id="toggleSuppressionCuve"><i class="bi-trash-fill"></i></button>
      </div>
      <div class="row row-cols-1 row-cols-sm-1 row-cols-md-2 row-cols-lg-2 row-cols-xl-3" id="listCuves"> </div>

      <div class="modal fade" id="addQuantiteModal" tabindex="-1" role="dialog" aria-labelledby="addQuantiteModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">Ajouter une quantité à la cuve <span id="modal_cuve_id">X</span></h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form>
                <div class="form-group">
                  <label for="sumQuantity" class="col-form-label">Quantité à ajouter (<b>en CL</b>):</label>
                  <input type="number" class="form-control" id="sumQuantity">
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Fermer</button>
              <button type="button" class="btn btn-primary" data-dismiss="modal" onclick="addCuveQuantity($('#modal_cuve_id').html(), $('#sumQuantity').val())">Ajouter</button>
            </div>
          </div>
        </div>
      </div>
      `);
    sendMessage("ask|cuves");
  }else if(page=="reglages"){
    $("#page").html(`<h1>Réglages</h1>
                    <div id="reglages">
                    </div>`);
    sendMessage("ask|reglages");
  }
  if ($(window).width() <= 800) {
    $('.navbar-toggler:not(.collapsed)').click();
  }
}

function showBoissonModele(isNew, id, nomAffichage, nomCourt , couleur,  pourcentageAlcool, logo){
  $("#page").html(`
    <h1>`+(isNew ? "Nouvelle boisson" : ("Modification de la boisson " + id))+`</h1>
    <div class="jumbotron mx-auto" style="padding:2rem; max-width: 600px;">
    <form action="javascript:updateBoisson(${isNew}, ${id})" id="formBoisson">
      <div class="form-group">
        <label for="nomAffichage">Nom complet</label>
        <input type="text" value="${nomAffichage}" class="form-control" id="nomAffichage" placeholder="Nom d'affichage complet">
      </div>
      <div class="form-group">
        <label for="nomCourt">Nom court</label>
        <input type="text" value="${nomCourt}" class="form-control" id="nomCourt" placeholder="Sans espace">
      </div>
      <div class="form-group">
        <label for="nomCourt">Couleur de la boisson</label>
        <input type="color" value="${couleur}" class="form-control" id="couleur">
      </div>
      <div class="form-group">
        <label for="nomCourt">Pourcentage d'alcool de la boisson</label>
        <input type="number" value="${pourcentageAlcool}" step="0.01" class="form-control" id="pourcentageAlcool" placeholder="0 si non alcoolisé, séparé par un .">
      </div>
      <div class="form-group">
        ` + (logo!="" ? ('<img style="height:70px; width:70px;" src="'+logo+'" class="align-self-center mr-3">') : '') + `
        <label for="nomCourt">Logo de la boisson (.png)</label>
        <input type="file" class="form-control" accept="image/png" id="logo">
      </div>
      <button type="submit" class="btn btn-primary btn-block" id="btn">`+(isNew ? "Créer" : "Modifier")+`</button>
    </form>
    </div>
    `);
}

function addCuveAccueil(num, name, color, level, enabled, running){
  blur = (Boolean(parseInt(enabled)) ? "" : " blur");
  glowing = (Boolean(parseInt(running)) ? " glowing" : "");
  $("#listCuves").append(`
    <div class="col-xs-4 tinyCuve${blur}" id="cuve_${num}">
      <div class="card text-center" style="width: 7.2rem;">
        <div class="glowingDiv${glowing}" style="position:absolute; width:100%; height:100%;color: ${color};"/>
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
          <div class="btn-group btn-group-toggle" data-toggle="buttons" style="padding-top:20px">
            <label class="pompe-on btn btn-secondary btn-sm${(Boolean(parseInt(running)) ? " disabled" : "")}">
              <input type="radio" name="options" id="option1" onclick="sendMessage('toggle|pompe|${num}|1')"> On
            </label>
            <label class="pompe-off btn btn-secondary btn-sm${(Boolean(parseInt(running)) ? "" : " disabled")}">
              <input type="radio" name="options" id="option2" onclick="sendMessage('toggle|pompe|${num}|0')"> Off
            </label>
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

function addBoisson(id, nomAffichage, nomCourt, couleur, pourcentageAlcool, editing, logo){
  hideDelete = " hide"
  hideModify = ""
  editing = Boolean(parseInt(editing))
  if ($("#toggleSuppressionBoisson").hasClass("btn-danger")){
      hideDelete = ""
      hideModify = " hide"
  }

  $("#listBoissons").append(`
    <div class="col" id="boisson_${id}">
      <div class="card" style="margin-bottom:10px;word-wrap:unset;padding:5px;">
        <div class="card-body" style="padding:0;padding-right: 10px;padding-left: 10px;">
          <div class="boisson_hide `+(editing ? "" : "hide")+`" style="position: absolute;top: 0;left: 0;width: 100%;height: 100%;z-index: 1;display: flex;justify-content: center;align-items: center;border-radius:5px;background-color:#5f59597a;">
              <p style="margin-bottom: 0; font-weight: 700;text-shadow: 0 0 5px #ff0000;">En cours de modification...</p>
          </div>
          <form id="data_boisson_${id}">
            <input type="hidden" id="id" value="${id}">
            <input type="hidden" id="nomAffichage" value="${nomAffichage}">
            <input type="hidden" id="nomCourt" value="${nomCourt}">
            <input type="hidden" id="couleur" value="${couleur}">
            <input type="hidden" id="pourcentageAlcool" value="${pourcentageAlcool}">
            <input type="hidden" id="logo" value="${logo}">
          </form>
          <div class="media `+(editing ? "blur" : "")+`">
            <img style="height:70px; width:70px;" src="${logo}" class="align-self-center mr-3" id="logo_boisson">
            <div class="media-body align-self-center">
              <div class="row">
                <div class="col">
                  <h5 class="mt-0" id="nomAffichage_boisson">${nomAffichage}</h5><span id="text_alcool_boisson">`+ ((parseInt(pourcentageAlcool)==0) ? "" : pourcentageAlcool + "° d'alcool") + `</span>
                </div>
                <div class="col align-self-center text-right">
                  <button type="button" class="btn btn-secondary btn-modify-boisson${hideModify}" onclick="setPage('modifyBoisson', ${id})">Modifier</button>
                  <button type="button" class="btn btn-danger btn-delete-boisson${hideDelete}" onclick="deleteBoisson(${id})">Supprimer</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    `);
}

function addBoissonSelect(id, nomAffichage, nomCourt, couleur, pourcentageAlcool, editing, logo){
  hideDelete = " hide"
  hideModify = ""
  editing = Boolean(parseInt(editing))
  if ($("#toggleSuppressionBoisson").hasClass("btn-danger")){
      hideDelete = ""
      hideModify = " hide"
  }

  $("#listBoissons").append(`
    <div class="col" id="boisson_${id}">
      <div class="card highlightOnHover" style="margin-bottom:10px;word-wrap:unset;padding:5px;" onClick="selectBoisson(${id})">
        <div class="card-body" style="padding:0;padding-right: 10px;padding-left: 10px;">
          <div class="boisson_hide `+(editing ? "" : "hide")+`" style="position: absolute;top: 0;left: 0;width: 100%;height: 100%;z-index: 1;display: flex;justify-content: center;align-items: center;border-radius:5px;background-color:#5f59597a;">
              <p style="margin-bottom: 0; font-weight: 700;text-shadow: 0 0 5px #ff0000;">En cours de modification...</p>
          </div>
          <div class="media `+(editing ? "blur" : "")+`">
            <img style="height:70px; width:70px;" src="${logo}" class="align-self-center mr-3" id="logo_boisson">
            <div class="media-body align-self-center">
              <div class="row">
                <div class="col">
                  <h5 class="mt-0" id="nomAffichage_boisson">${nomAffichage}</h5><span id="text_alcool_boisson">`+ ((parseInt(pourcentageAlcool)==0) ? "" : pourcentageAlcool + "° d'alcool") + `</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    `);
}

function selectBoisson(id){
  $("#selectedBoisson .highlightOnHover").attr('id', 'boisson_'+id)
  $("#selectedBoisson #bId").val(id)
  sendMessage("ask|updateBoisson|"+id)
  $("#selectBoissonModal").modal("hide");
}

function modifyBoisson(dataSource){
  var id = $(dataSource + " #id").val()
  var nomCourt = $(dataSource + " #nomCourt").val()
  var nomAffichage = $(dataSource + " #nomAffichage").val()
  var couleur = $(dataSource + " #couleur").val()
  var pourcentageAlcool = $(dataSource + " #pourcentageAlcool").val()
  var logo = $(dataSource + " #logo").val()

  sendMessage("editing|boisson|" + id + "|1");
  showBoissonModele(false, id, nomAffichage, nomCourt , couleur,  pourcentageAlcool, logo)
}

function deleteBoisson(id){
  sendMessage("delete|boisson|" + id);
}

function updateBoisson(isNew, id){
  $("#formBoisson #btn").attr("disabled", "true")
  setTimeout(function(){
  $("#formBoisson #btn").removeAttr("disabled")
  }, 1000);
  var nomCourt = $("#formBoisson #nomCourt").val()
  var nomAffichage = $("#formBoisson #nomAffichage").val()
  var couleur = $("#formBoisson #couleur").val()
  var pourcentageAlcool = $("#formBoisson #pourcentageAlcool").val()

  image = $("#formBoisson #logo").prop('files')[0]

  if(image!=undefined){
    var reader = new FileReader();
    var rawData = new ArrayBuffer();

    reader.onload = function(e) {
        rawData = e.target.result;
        if(isNew){
          sendMessage("add|boisson|" + nomAffichage + "|" + nomCourt  + "|" + couleur  + "|" +  pourcentageAlcool  + "|" + rawData);
        }else{
          sendMessage("update|" + id + "|boisson|" + nomAffichage + "|" + nomCourt  + "|" + couleur  + "|" +  pourcentageAlcool  + "|" + rawData);
        }
    }
    reader.readAsDataURL(image);
  }else{
    if(isNew){
      sendMessage("add|boisson|" + nomAffichage + "|" + nomCourt  + "|" + couleur  + "|" +  pourcentageAlcool  + "| ");
    }else{
      sendMessage("update|" + id + "|boisson|" + nomAffichage + "|" + nomCourt  + "|" + couleur  + "|" +  pourcentageAlcool  + "|");
    }
  }
}

function toggleSuppressionBoisson(){
  $(".btn-delete-boisson").toggleClass("hide");
  $(".btn-modify-boisson").toggleClass("hide");
  $("#toggleSuppressionBoisson").toggleClass("btn-outline-danger")
  $("#toggleSuppressionBoisson").toggleClass("btn-danger")
}

function toggleCantEditBoisson(id, etat){
  if(etat){
    $("#boisson_"+id+" .boisson_hide").removeClass("hide");
    $("#boisson_"+id+" .media").addClass("blur");
  }else{
    $("#boisson_"+id+" .boisson_hide").addClass("hide");
    $("#boisson_"+id+" .media").removeClass("blur");
  }
}

function showPopupAddQuantite(id){
  $("#modal_cuve_id").html(id)
  $("#addQuantiteModal").modal("show");
}

function showPopupSelectBoisson(){
  $("#listBoissons").html("");
  $("#selectBoissonModal").modal("show");
  $('.modal').css('overflow-y', 'auto');
  sendMessage("ask|boissons");
}

function modifyCuve(dataSource){
  var id = $(dataSource + " #id").val()
  var quantite = $(dataSource + " #quantite").val()
  var quantiteMax = $(dataSource + " #quantiteMax").val()
  var pompePinId = $(dataSource + " #pompePinId").val()
  var dmPinId = $(dataSource + " #dmPinId").val()
  var debitmetreMlParTick = $(dataSource + " #debitmetreMlParTick").val()
  var bId = $(dataSource + " #bId").val()

  sendMessage("editing|cuve|" + id + "|1");
  showCuveModele(false, id, quantite, quantiteMax, pompePinId, dmPinId, debitmetreMlParTick, bId)
}

function toggleSuppressionCuve(){
  $(".btn-delete-cuve").toggleClass("hide");
  $(".btn-modify-cuve").toggleClass("hide");
  $(".btn-toggle-cuve").toggleClass("hide");
  $("#toggleSuppressionCuve").toggleClass("btn-outline-danger")
  $("#toggleSuppressionCuve").toggleClass("btn-danger")
}

function addCuve(id, quantite, quantiteMax, niveau, pompePinId, dmPinId, debitmetreMlParTick, bId, bNomAffiche, bNomCourt, bCouleur, editing, enabled, running){
    hideDelete = " hide"
    hideModify = ""
    editing = Boolean(parseInt(editing))
    enabled = Boolean(parseInt(enabled))
    if ($("#toggleSuppressionCuve").hasClass("btn-danger")){
        hideDelete = ""
        hideModify = " hide"
    }
    glowing = (Boolean(parseInt(running)) ? " glowing" : "");

    $("#listCuves").append(`
      <div class="col" id="cuve_${id}">
        <div class="card" style="margin-bottom:10px;word-wrap:unset;padding:5px;">
          <div class="glowingDiv${glowing}" style="position:absolute; width:100%; height:100%;color: ${bCouleur};"/>
          <div class="card-body" style="padding:0;padding-right: 10px;padding-left: 10px;">
            <div class="cuve_hide `+(editing ? "" : "hide")+`" style="position: absolute;top: 0;left: 0;width: 100%;height: 100%;z-index: 1;display: flex;justify-content: center;align-items: center;border-radius:5px;background-color:#5f59597a;">
                <p style="margin-bottom: 0; font-weight: 700;text-shadow: 0 0 5px #ff0000;">En cours de modification...</p>
            </div>
            <form id="data_cuve_${id}">
              <input type="hidden" id="id" value="${id}">
              <input type="hidden" id="quantite" value="${quantite}">
              <input type="hidden" id="quantiteMax" value="${quantiteMax}">
              <input type="hidden" id="niveau" value="${niveau}">
              <input type="hidden" id="pompePinId" value="${pompePinId}">
              <input type="hidden" id="dmPinId" value="${dmPinId}">
              <input type="hidden" id="debitmetreMlParTick" value="${debitmetreMlParTick}">
              <input type="hidden" id="bId" value="${bId}">
              <input type="hidden" id="bNomAffiche" value="${bNomAffiche}">
              <input type="hidden" id="bNomCourt" value="${bNomCourt}">
              <input type="hidden" id="bCouleur" value="${bCouleur}">
            </form>
            <div class="media `+(editing ? "blur" : "")+`">
              <div class="media-body">

                <div class="row">
                  <div class="text-center" style="flex:1">
                    <h4>${id}# <span id="cuve-${id}-name">${bNomCourt}</span></h4>
                  </div>
                </div>

                <div class="row" style="margin-top:15px;margin-bottom:15px;">
                  <div class="col text-center align-self-center" style="left:18px">
                    <div class="banner">
                      <div class="fill" id="cuve-${id}-level" style="transform: translate(0, 250px);">
                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="300px" height="300px" viewBox="0 0 300 300" enable-background="new 0 0 300 300" xml:space="preserve">
                          <path id="cuve-${id}-color" class="waveShape" style="fill: ${bCouleur};" d="M300,300V2.5c0,0-0.6-0.1-1.1-0.1c0,0-25.5-2.3-40.5-2.4c-15,0-40.6,2.4-40.6,2.4
                      c-12.3,1.1-30.3,1.8-31.9,1.9c-2-0.1-19.7-0.8-32-1.9c0,0-25.8-2.3-40.8-2.4c-15,0-40.8,2.4-40.8,2.4c-12.3,1.1-30.4,1.8-32,1.9
                      c-2-0.1-20-0.8-32.2-1.9c0,0-3.1-0.3-8.1-0.7V300H300z" />
                        </svg>
                      </div>
                    </div>
                  </div>
                  <div class="col text-center align-self-center" style="font-size: 0.9em; line-height: 15px; flex:2;">
                    <p><b>Quantité / Max</b><br>
                    <span id="text_quantite_cuve">${quantite}</span> / <span id="text_quantiteMax_cuve">${quantiteMax}</span></p>
                    <p><b>Pin de la pompe</b><br>
                    <span id="text_pompePinId_cuve">${pompePinId}</span></p>
                    <p><b>Pin du débitmètre</b><br>
                    <span id="text_dmPinId_cuve">${dmPinId}</span><p>
                    <p><b>mL par Tick du débitmètre</b><br>
                    <span id="text_debitmetreMlParTick_cuve">${debitmetreMlParTick}</span><p>
                  </div>
                  <div class="col align-self-center">
                    <button type="button" id="button_700_cuve" onclick="addCuveQuantity(${id}, 700)" class="btn btn-outline-info btn-sm btn-block"`+((parseInt(quantite)+700)>parseInt(quantiteMax) ? ' disabled' : '')+`>+70CL</button>
                    <button type="button" id="button_750_cuve" onclick="addCuveQuantity(${id}, 750)" class="btn btn-outline-info btn-sm btn-block"`+((parseInt(quantite)+750)>parseInt(quantiteMax) ? ' disabled' : '')+`>+75CL</button>
                    <button type="button" id="button_1000_cuve" onclick="addCuveQuantity(${id}, 1000)" class="btn btn-outline-info btn-sm btn-block"`+((parseInt(quantite)+1000)>parseInt(quantiteMax) ? ' disabled' : '')+`>+1L</button>
                    <button type="button" id="button_1500_cuve" onclick="addCuveQuantity(${id}, 1500)" class="btn btn-outline-info btn-sm btn-block"`+((parseInt(quantite)+1500)>parseInt(quantiteMax) ? ' disabled' : '')+`>+1.5L</button>
                    <button type="button" id="button_2000_cuve" onclick="addCuveQuantity(${id}, 2000)" class="btn btn-outline-info btn-sm btn-block"`+((parseInt(quantite)+2000)>parseInt(quantiteMax) ? ' disabled' : '')+`>+2L</button>
                    <button type="button" id="button_more_cuve" class="btn btn-info btn-sm btn-block" onclick="showPopupAddQuantite(${id})"`+(parseInt(quantite)>=parseInt(quantiteMax) ? ' disabled' : '')+`>...</button>
                  </div>
                </div>

                <div class="row">
                  <div class="col align-self-center text-center">
                    <button type="button" class="btn btn-secondary btn-modify-cuve${hideModify}" onclick="setPage('modifyCuve', ${id})">Modifier</button>
                    <button type="button" class="btn btn-danger btn-delete-cuve${hideDelete}" onclick="deleteCuve(${id})">Supprimer</button>
                    `+ (enabled ? `<button type="button" class="btn btn-warning btn-toggle-cuve${hideModify}" onclick="toggleCuve(${id}, 0)">Désactiver</button>`
                             : `<button type="button" class="btn btn-success btn-toggle-cuve${hideModify}" onclick="toggleCuve(${id}, 1)">Activer</button>` ) +
                  `</div>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
      `);

      setTimeout(function(){
        $("#cuve-"+id+"-level").css("transform", "translate(0,"+niveau+"px)")
      }, 10);
}

function showCuveModele(isNew, id, quantite, quantiteMax, pompePinId, dmPinId, debitmetreMlParTick, bId){
  $("#page").html(`
    <h1>`+(isNew ? "Nouvelle cuve" : ("Modification de la cuve " + id))+`</h1>
    <div class="jumbotron mx-auto" style="padding:2rem; max-width: 600px;">
    <form action="javascript:updateCuve(${isNew}, ${id})" id="formCuve">
      <div class="form-group" id="selectedBoisson">
        <input type="hidden" id="bId" value="${bId}">
        <label>Boisson contenue</label>
          <div class="card highlightOnHover" id="boisson_${bId}" onclick="showPopupSelectBoisson()" style="margin-bottom:10px;word-wrap:unset;padding:5px;">
            <div class="card-body" style="padding:0;padding-right: 10px;padding-left: 10px;">
              <div class="boisson_hide hide" style="position: absolute;top: 0;left: 0;width: 100%;height: 100%;z-index: 1;display: flex;justify-content: center;align-items: center;border-radius:5px;background-color:#5f59597a;">
                  <p style="margin-bottom: 0; font-weight: 700;text-shadow: 0 0 5px #ff0000;">En cours de modification...</p>
              </div>
              <div class="media">
                <img style="height:70px; width:70px;" src="" class="align-self-center mr-3" id="logo_boisson">
                <div class="media-body align-self-center">
                  <div class="row">
                    <div class="col">
                      <h5 class="mt-0" id="nomAffichage_boisson">Boisson</h5><span id="text_alcool_boisson">`+(parseInt(bId)=="-1" ? "Boisson non sélectionnée" : "Chargement...")+`</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
      </div>
      <div class="form-group">
        <label for="quantite">Quantité actuelle</label>
        <input type="number" value="${quantite}" class="form-control" id="quantite" step="0.01" placeholder="0">
      </div>
      <div class="form-group">
        <label for="quantiteMax">Quantité maximum</label>
        <input type="number" value="${quantiteMax}" class="form-control" id="quantiteMax" step="0.01" placeholder="5000">
      </div>
      <div class="form-group">
        <label for="pompePinId">Pin de la pompe</label>
        <input type="number" value="${pompePinId}" class="form-control" id="pompePinId" placeholder="0">
      </div>
      <div class="form-group">
        <label for="dmPinId">Pin du débitmètre</label>
        <input type="number" value="${dmPinId}" class="form-control" id="dmPinId" placeholder="0">
      </div>
      <div class="form-group">
        <label for="debitmetreMlParTick">Nombre de ML par Tick du débitmètre</label>
        <input type="number" value="${debitmetreMlParTick}" class="form-control" id="debitmetreMlParTick" step="0.01" placeholder="0">
      </div>
      <button type="submit" class="btn btn-primary btn-block" id="btn">`+(isNew ? "Créer" : "Modifier")+`</button>
    </form>
    </div>

    <div class="modal fade" id="selectBoissonModal" tabindex="-1" role="dialog" aria-labelledby="selectBoissonModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Sélectionne la boisson contenue dans la cuve</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="row row-cols-1" id="listBoissons"> </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Fermer</button>
          </div>
        </div>
      </div>
    </div>
    `);

    sendMessage("ask|updateBoisson|" + bId);
}

function updateCuve(isNew, id){
  $("#formCuve #btn").attr("disabled", "true")
  setTimeout(function(){
  $("#formCuve #btn").removeAttr("disabled")
  }, 1000);

  var quantite = $("#formCuve #quantite").val()
  var quantiteMax = $("#formCuve #quantiteMax").val()
  var pompePinId = $("#formCuve #pompePinId").val()
  var dmPinId = $("#formCuve #dmPinId").val()
  var debitmetreMlParTick = $("#formCuve #debitmetreMlParTick").val()
  var bId = $("#formCuve #bId").val()

  if(isNew){
    sendMessage("add|cuve|" + quantite + "|" + quantiteMax  + "|" + pompePinId  + "|" +  dmPinId  + "|" + debitmetreMlParTick + "|" + bId);
  }else{
    sendMessage("update|" + id + "|cuve|" + quantite + "|" + quantiteMax  + "|" + pompePinId  + "|" +  dmPinId  + "|" + debitmetreMlParTick + "|" + bId);
  }
}

function deleteCuve(id) {
  sendMessage("delete|cuve|" + id);
}

function toggleCantEditCuve(id, etat){
  if(etat){
    $("#cuve_"+id+" .cuve_hide").removeClass("hide");
    $("#cuve_"+id+" .media").addClass("blur");
  }else{
    $("#cuve_"+id+" .cuve_hide").addClass("hide");
    $("#cuve_"+id+" .media").removeClass("blur");
  }
}

function addCuveQuantity(id, quantity){
  sendMessage(`addCuveQuantity|${id}|${quantity}`);
}

function toggleCuve(id, toggle){
  sendMessage(`toggle|cuve|${id}|${toggle}`);
}

function addReglages(id, nomCourt, nomAffichage){
  $("#reglages").append(`
    <div class="row" style="padding-top:10px" id="reglages_${id}">
      <div class="card w-100">
        <div class="card-body">
          <h5 class="card-title">${nomAffichage}</h5>
          <h6 class="card-subtitle mb-2 text-muted">${nomCourt}</h6>
          <p class="card-text"></p>
        </div>
      </div>
    </div>
  `);
}

function addReglage(id, type, nomCourt, nomAffichage, value, groupeId){
  if(type == "int"){
    $("#reglages_"+groupeId+" .card-text").append(`
      <div class="form-row text-center align-items-center" style="padding-left:25px;padding-right:25px;">
        <label class="col-sm-2 col-form-label" for="reglage_${id}"><span>${nomAffichage}</span><br><span class="text-muted">${nomCourt}</span></label>
        <div class="col">
          <input type="number" class="form-control" id="reglage_${id}" value="${value}">
        </div>
        <button class="btn btn-primary col-sm-2" style="margin:5px;" onclick="updateReglage(${groupeId}, ${id}, $('#reglage_${id}').val())">Valider</button>
      </div>
      `);
  }else if(type=="color"){
      $("#reglages_"+groupeId+" .card-text").append(`
        <div class="form-row text-center align-items-center" style="padding-left:25px;padding-right:25px;">
          <label class="col-sm-2 col-form-label" for="reglage_${id}"><span>${nomAffichage}</span><br><span class="text-muted">${nomCourt}</span></label>
          <div class="col">
            <input type="color" class="form-control" id="reglage_${id}" value="${value}">
          </div>
          <button class="btn btn-primary col-sm-2" style="margin:5px;" onclick="updateReglage(${groupeId}, ${id}, $('#reglage_${id}').val())">Valider</button>
        </div>
        `);
  }else{
    $("#reglages_"+groupeId+" .card-text").append(`
      <div class="form-row text-center align-items-center" style="padding-left:25px;padding-right:25px;">
        <label class="col-sm-2 col-form-label" for="reglage_${id}"><span>${nomAffichage}</span><br><span class="text-muted">${nomCourt}</span></label>
        <div class="col">
          <span>${value}</span> <span class="text-muted"> (type inconnu : ${type})</span>
        </div>
        <button disabled class="btn btn-primary col-sm-2" style="margin:5px;">Valider</button>
      </div>
      `);
  }
}

function updateReglage(groupeId, id, value){
  sendMessage(`update|reglage|${groupeId}|${id}|${value}`);
}

$( document ).ready(function() {
  setTimeout(function(){
    connexionServeur();
  }, 500);
});
