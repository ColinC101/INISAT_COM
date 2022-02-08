//document.getElementById("coup_").innerHTML = (".").fontcolor("white");
//document.getElementById("roue_").innerHTML = (".").fontcolor("white");


// FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS 

  function dateHeure(){   // fonction pour renvoyer la date et l'heure actuelle
    var today = new Date();
    var date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = time+' '+date;
    return dateTime;
  }
 

  function testCam1() {
  if (localStorage.getItem("camStatus")==1) { var myWindow = window.open("http://192.168.4.183/capture","Capture", "width=800px, height=600px, menubar=no, directories=no, location=no, scrollbars=no, status =no, status = no");}
  else { var myWindow = window.open("camoff.html","Cam Off", "width=1200px, height=800px,menubar=no, directories=no, location=no, scrollbars=no, status =no, status = no");}
  }
  
  function testCam2() {
  if (localStorage.getItem("camStatus")==1) { var myWindow = window.open("http://192.168.4.183:81/stream","Stream", "width=800px, height=600px, menubar=no, directories=no, location=no, scrollbars=no, status =no, status = no" );}
  else { var myWindow = window.open("camoff.html","Cam Off", " width=1200px, height=800px, menubar=no, directories=no, location=no, scrollbars=no, status =no, status = no");}
  }


  // fonctions pour la partie Roue a Inertie

  function validateFormI1() {
    var speed = document.forms["myFormI1"]["vitesse"].value;
    var sens = document.forms["myFormI1"]["sens"].value;
   // var SP = (speed).padStart(4, "0");
    
    if ((speed<0) || (speed>100)) {

      document.getElementById("roue_").innerHTML = ("Veuillez choisir une valeur entre 0 et 100 % !").fontcolor("red"); 
    }
    else {

      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        var obj = this.responseText;
        document.getElementById("roue_").innerHTML = (".").fontcolor("white");
        setTimeout(function(){document.getElementById("roue_").innerHTML = (obj).fontcolor("green"); },100);
        }}
      xhr.open("GET", "/roue?choix="+(sens+speed), true);
      xhr.send();
    }
  }

  function stopFormI1() {
    var stop ="S"
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("roue_").innerHTML = (".").fontcolor("white");
      setTimeout(function(){document.getElementById("roue_").innerHTML = (obj).fontcolor("green"); },100);
      }}
    xhr.open("GET", "/roue?choix="+stop, true);
    xhr.send();
    document.forms["myFormI1"]["vitesse"].value = 0;

  }
  
  // Fonction pour la validation du formulaireT1 dans la page Télécommandes (rotation coupleur)

  function validateFormT1() {
    var A_coup = document.forms["myFormT1"]["an_coup"].value;
    if ((A_coup<-30) || (A_coup>30) || (A_coup==0)) {
      console.log('%c%s','color: red; font-size: 12px', dateHeure());
      console.log("%cVeuillez choisir une valeur entre -30 et 30 !","color:orange;font-size: 12px; font-weight:bold");
      document.getElementById("coup_").innerHTML = ("Veuillez choisir une valeur entre -30 et 30° !").fontcolor("red"); 
    }
    else {
      console.log('%c%s','color: red; font-size: 12px', dateHeure());
      console.log("%cL\'angle choisi est : %s°","color:green;font-size: 12px; font-weight:bold",A_coup)
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        var obj = this.responseText;
        document.getElementById("coup_").innerHTML = (".").fontcolor("white");
        setTimeout(function(){document.getElementById("coup_").innerHTML = (obj).fontcolor("green"); },100);
        }}
      xhr.open("GET", "/ang_couple?choix="+A_coup, true);
      xhr.send();
    }
  }
  
function demagnetisation() {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var obj = this.responseText;
    document.getElementById("dmag_").innerHTML = (".").fontcolor("white");
    setTimeout(function(){document.getElementById("dmag_").innerHTML = (obj).fontcolor("green"); },100);
    }}
  xhr.open("GET", "/demag", true);
  xhr.send();
  document.getElementById("S1V1").disabled = true;
  document.getElementById("S1V1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S1V1").style.cursor = "none";
  document.getElementById("S1V2").disabled = true;
  document.getElementById("S1V2").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S1V2").style.cursor = "none";
  document.getElementById("S2V1").disabled = true;
  document.getElementById("S2V1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S2V1").style.cursor = "none";
  document.getElementById("S2V2").disabled = true;
  document.getElementById("S2V2").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S2V2").style.cursor = "none";
  document.getElementById("tstStp").disabled = true;
  document.getElementById("tstStp").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("tstStp").style.cursor = "none";

  document.getElementById("SubT1").disabled = true;   // desactiver le bouton envoyer de la rotatoion magnéto
  document.getElementById("SubT1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("SubT1").style.cursor = "none";

  document.getElementById("dMag").disabled = true;  // desactiver le bouton envoyer de la démagnétisation
  document.getElementById("dMag").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("dMag").style.cursor = "none";
}

function testS1V1() {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var obj = this.responseText;
    document.getElementById("tst_").innerHTML = (".").fontcolor("white");
    setTimeout(function(){document.getElementById("tst_").innerHTML = (obj).fontcolor("green"); },100);
    }}
  xhr.open("GET", "/tst1", true);
  xhr.send();
  document.getElementById("S1V1").disabled = true;
  document.getElementById("S1V1").style.backgroundColor = "#FFA07A";
  document.getElementById("S1V1").style.cursor = "none";
  document.getElementById("S1V2").disabled = true;
  document.getElementById("S1V2").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S1V2").style.cursor = "none";
  document.getElementById("S2V1").disabled = true;
  document.getElementById("S2V1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S2V1").style.cursor = "none";
  document.getElementById("S2V2").disabled = true;
  document.getElementById("S2V2").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S2V2").style.cursor = "none";
  document.getElementById("tstStp").disabled = false;
  document.getElementById("tstStp").style.backgroundColor = "#003366";
  document.getElementById("tstStp").style.cursor = "pointer";

  document.getElementById("SubT1").disabled = true;   // desactiver le bouton envoyer de la rotatoion magnéto
  document.getElementById("SubT1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("SubT1").style.cursor = "none";

  document.getElementById("dMag").disabled = true;  // desactiver le bouton envoyer de la démagnétisation
  document.getElementById("dMag").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("dMag").style.cursor = "none";


}

function testS1V2() {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var obj = this.responseText;
    document.getElementById("tst_").innerHTML = (".").fontcolor("white");
    setTimeout(function(){document.getElementById("tst_").innerHTML = (obj).fontcolor("green"); },100);
    }}
  xhr.open("GET", "/tst2", true);
  xhr.send();
  document.getElementById("S1V1").disabled = true;
  document.getElementById("S1V1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S1V1").style.cursor = "none";
  document.getElementById("S1V2").disabled = true;
  document.getElementById("S1V2").style.backgroundColor = "#FFA07A";
  document.getElementById("S1V2").style.cursor = "none";
  document.getElementById("S2V1").disabled = true;
  document.getElementById("S2V1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S2V1").style.cursor = "none";
  document.getElementById("S2V2").disabled = true;
  document.getElementById("S2V2").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S2V2").style.cursor = "none";
  document.getElementById("tstStp").disabled = false;
  document.getElementById("tstStp").style.backgroundColor = "#003366";
  document.getElementById("tstStp").style.cursor = "pointer";

  document.getElementById("SubT1").disabled = true;   // desactiver le bouton envoyer de la rotatoion magnéto
  document.getElementById("SubT1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("SubT1").style.cursor = "none";

  document.getElementById("dMag").disabled = true;  // desactiver le bouton envoyer de la démagnétisation
  document.getElementById("dMag").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("dMag").style.cursor = "none";
}
function testS2V1() {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var obj = this.responseText;
    document.getElementById("tst_").innerHTML = (".").fontcolor("white");
    setTimeout(function(){document.getElementById("tst_").innerHTML = (obj).fontcolor("green"); },100);
    }}
  xhr.open("GET", "/tst3", true);
  xhr.send();
  document.getElementById("S1V1").disabled = true;
  document.getElementById("S1V1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S1V1").style.cursor = "none";
  document.getElementById("S1V2").disabled = true;
  document.getElementById("S1V2").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S1V2").style.cursor = "none";
  document.getElementById("S2V1").disabled = true;
  document.getElementById("S2V1").style.backgroundColor = "#FFA07A";
  document.getElementById("S2V1").style.cursor = "none";
  document.getElementById("S2V2").disabled = true;
  document.getElementById("S2V2").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S2V2").style.cursor = "none";
  document.getElementById("tstStp").disabled = false;
  document.getElementById("tstStp").style.backgroundColor = "#003366";
  document.getElementById("tstStp").style.cursor = "pointer";

  document.getElementById("SubT1").disabled = true;   // desactiver le bouton envoyer de la rotatoion magnéto
  document.getElementById("SubT1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("SubT1").style.cursor = "none";

  document.getElementById("dMag").disabled = true;  // desactiver le bouton envoyer de la démagnétisation
  document.getElementById("dMag").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("dMag").style.cursor = "none";
}
function testS2V2() {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var obj = this.responseText;
    document.getElementById("tst_").innerHTML = (".").fontcolor("white");
    setTimeout(function(){document.getElementById("tst_").innerHTML = (obj).fontcolor("green"); },100);
    }}
  xhr.open("GET", "/tst4", true);
  xhr.send();
  document.getElementById("S1V1").disabled = true;
  document.getElementById("S1V1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S1V1").style.cursor = "none";
  document.getElementById("S1V2").disabled = true;
  document.getElementById("S1V2").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S1V2").style.cursor = "none";
  document.getElementById("S2V1").disabled = true;
  document.getElementById("S2V1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("S2V1").style.cursor = "none";
  document.getElementById("S2V2").disabled = true;
  document.getElementById("S2V2").style.backgroundColor = "#FFA07A";
  document.getElementById("S2V2").style.cursor = "none";
  document.getElementById("tstStp").disabled = false;
  document.getElementById("tstStp").style.backgroundColor = "#003366";
  document.getElementById("tstStp").style.cursor = "pointer";

  document.getElementById("SubT1").disabled = true;   // desactiver le bouton envoyer de la rotatoion magnéto
  document.getElementById("SubT1").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("SubT1").style.cursor = "none";

  document.getElementById("dMag").disabled = true;  // desactiver le bouton envoyer de la démagnétisation
  document.getElementById("dMag").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("dMag").style.cursor = "none";
}

// botton stop test magnéto déasactivé au début
document.getElementById("tstStp").disabled = true;
document.getElementById("tstStp").style.backgroundColor = "rgb(124, 124, 124)";
document.getElementById("tstStp").style.cursor = "none";

function testSTP() {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var obj = this.responseText;
    document.getElementById("tst_").innerHTML = (".").fontcolor("white");
    setTimeout(function(){document.getElementById("tst_").innerHTML = (obj).fontcolor("green"); },100);
    }}
  xhr.open("GET", "/tststp", true);
  xhr.send();

document.getElementById("tstStp").disabled = true;
document.getElementById("tstStp").style.backgroundColor = "rgb(124, 124, 124)";
document.getElementById("tstStp").style.cursor = "none";
  
}


// fonctions pour la partie Trajectoire GNSS

 

  function trajOn() {
    startGnss();
   document.getElementById("traj-on").disabled = true;
   document.getElementById("traj-on").style.backgroundColor = "rgb(124, 124, 124)";
   document.getElementById("traj-on").style.cursor = "none";  
   document.getElementById("traj-off").disabled = false;
   document.getElementById("traj-off").style.backgroundColor = "#67c26f";
   document.getElementById("traj-off").style.cursor = "pointer";
   document.getElementById("traj-save").disabled = true;
   document.getElementById("traj-save").style.backgroundColor = "rgb(124, 124, 124)";
   document.getElementById("traj-save").style.cursor = "none";  
  }

  function trajOff() {
    stopGnss();
    document.getElementById("traj-off").disabled = true;
    document.getElementById("traj-off").style.backgroundColor = "rgb(124, 124, 124)";
    document.getElementById("traj-off").style.cursor = "none";
    document.getElementById("traj-save").disabled = false;
    document.getElementById("traj-save").style.backgroundColor = "#003366";
    document.getElementById("traj-save").style.cursor = "pointer";
 
   }

   

   function trajSave() {
    saveGnss();
  //  document.getElementById("traj-save2").disabled = true;
  // document.getElementById("traj-save2").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("traj-on").disabled = false;
   document.getElementById("traj-on").style.backgroundColor = "#67c26f" ;
   document.getElementById("traj-on").style.cursor = "pointer";
  // document.getElementById("traj-off").disabled = true;
  // document.getElementById("traj-off").style.backgroundColor = "rgb(124, 124, 124)";
  // document.getElementById("traj-off").style.cursor = "none";

   }

   /*
   function trajSave() {
    var myFile= window.open("test.txt"); //, " width=1200px, height=800px,menubar=no, directories=no, location=no, scrollbars=no, status =no");

  //  document.getElementById("traj-save2").disabled = true;
  // document.getElementById("traj-save2").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("traj-on").disabled = false;
   document.getElementById("traj-on").style.backgroundColor = "#67c26f" ;
   document.getElementById("traj-on").style.cursor = "pointer";

   }

   */

 
   
  function startGnss() {
    var heure = dateHeure();
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("trajectoire_").innerHTML = (".").fontcolor("white");
      setTimeout(function(){document.getElementById("trajectoire_").innerHTML = (obj).fontcolor("green"); },100);
      }}
    xhr.open("GET", "/startgnss?choix="+heure, true);
    xhr.send();
  }

  function stopGnss() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("trajectoire_").innerHTML = (".").fontcolor("white");
      setTimeout(function(){document.getElementById("trajectoire_").innerHTML = (obj).fontcolor("green"); },100);
      }}
    xhr.open("GET", "/stopgnss", true);
    xhr.send();
  }


  function saveGnss() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("trajectoire_").innerHTML = (".").fontcolor("white");
      setTimeout(function(){document.getElementById("trajectoire_").innerHTML = (obj).fontcolor("green"); },100);
      }}
    xhr.open("GET", "/savegnss", true);
    xhr.send();
  }

  /*
  function startGnss (){
  
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/user", true);
  xhr.send();

}

*/

// EVENT FIN DEMAGNETISATION EVENT FIN DEMAGNETISATION EVENT FIN DEMAGNETISATION EVENT FIN DEMAGNETISATION EVENT FIN DEMAGNETISATION EVENT FIN DEMAGNETISATION 

if (!!window.EventSource) {
  var source = new EventSource('/events5');


source.addEventListener('fct_fin', function(e) {
  var obj = e.data;
  if (obj=="A"){
    
  document.getElementById("dmag_").innerHTML = (".").fontcolor("white");
  setTimeout(function(){document.getElementById("dmag_").innerHTML = ("Démagnetisation finie").fontcolor("blue"); },100);
  document.getElementById("S1V1").disabled = false;    // réactiver les bouton test
  document.getElementById("S1V1").style.backgroundColor = "#FFA07A";
  document.getElementById("S1V1").style.cursor = "pointer";
  document.getElementById("S1V2").disabled = false;
  document.getElementById("S1V2").style.backgroundColor = "#FFA07A";
  document.getElementById("S1V2").style.cursor = "pointer";
  document.getElementById("S2V1").disabled = false;
  document.getElementById("S2V1").style.backgroundColor = "#FFA07A";
  document.getElementById("S2V1").style.cursor = "pointer";
  document.getElementById("S2V2").disabled = false;
  document.getElementById("S2V2").style.backgroundColor = "#FFA07A";
  document.getElementById("S2V2").style.cursor = "pointer";
  document.getElementById("tstStp").disabled = true;
  document.getElementById("tstStp").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("tstStp").style.cursor = "none";

  document.getElementById("SubT1").disabled = false;  // réactiver le bouton rotation
  document.getElementById("SubT1").style.backgroundColor = "#003366";
  document.getElementById("SubT1").style.cursor = "pointer";

  document.getElementById("dMag").disabled = false; // réactiver le bouton demagnétisation
  document.getElementById("dMag").style.backgroundColor = "#003366";
  document.getElementById("dMag").style.cursor = "pointer";
              }

  if (obj=="B"){
  document.getElementById("tst_").innerHTML = (".").fontcolor("white");
  setTimeout(function(){document.getElementById("tst_").innerHTML = ("Test fini").fontcolor("blue"); },100);
  document.getElementById("S1V1").disabled = false;    // réactiver les bouton test
  document.getElementById("S1V1").style.backgroundColor = "#FFA07A";
  document.getElementById("S1V1").style.cursor = "pointer";
  document.getElementById("S1V2").disabled = false;
  document.getElementById("S1V2").style.backgroundColor = "#FFA07A";
  document.getElementById("S1V2").style.cursor = "pointer";
  document.getElementById("S2V1").disabled = false;
  document.getElementById("S2V1").style.backgroundColor = "#FFA07A";
  document.getElementById("S2V1").style.cursor = "pointer";
  document.getElementById("S2V2").disabled = false;
  document.getElementById("S2V2").style.backgroundColor = "#FFA07A";
  document.getElementById("S2V2").style.cursor = "pointer";
  document.getElementById("tstStp").disabled = true;
  document.getElementById("tstStp").style.backgroundColor = "rgb(124, 124, 124)";
  document.getElementById("tstStp").style.cursor = "none";

  document.getElementById("SubT1").disabled = false;  // réactiver le bouton rotation
  document.getElementById("SubT1").style.backgroundColor = "#003366";
  document.getElementById("SubT1").style.cursor = "pointer";

  document.getElementById("dMag").disabled = false; // réactiver le bouton demagnétisation
  document.getElementById("dMag").style.backgroundColor = "#003366";
  document.getElementById("dMag").style.cursor = "pointer";
              }
}, false);
}