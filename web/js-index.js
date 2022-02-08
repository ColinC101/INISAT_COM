/*
window.addEventListener('load', (event) => {
  alert('Page loaded');

});
window.onload = function() { // same as window.addEventListener('load', (event) => {
  alert('Page loaded');

};
*/

// fonction a exécuter à l'ouverture de la page index.html pour lire les paramètres initiaux de la cam et l'interval
window.addEventListener('load', ouvPage());  

// Fonctions pour lire l'etat de la camera sur la carte Heltec au démarrage de la page
//var ouv = 0;
var cons_intv;
var gph_intv;
var camEtat;
var loraEtat;
function ouvPage(){
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
if (this.readyState == 4 && this.status == 200) {
var obj = JSON.parse(this.responseText);
console.log(obj);
camEtat = obj.cam;
cons_intv = obj.console_intv; 
gph_intv = obj.graph_intv; 
consf = obj.consf;
loraEtat =obj.lora;
sauveGarde ();
}}
xhr.open("GET", "/ouvPage", true);
xhr.send();

}
/*
window.addEventListener('unload', fermPage());  

function fermPage(){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/fermPage", true);
  xhr.send();
  }
/*
  window.onunload = function(){ // Alerte à la fermuture de la page
    var xhr = new XMLHttpRequest();
  xhr.open("GET", "/fermPage", true);
  xhr.send();
  }    
/*
ouv = this.responseText;
console.log(ouv);
camEtat = ouv.charAt(0);
INTV = ouv.substring(2);

*/

// Fonction pour enregistrer les paramètre de la can et l'interval dans localStorage, pour les partager vers les autres pages 
function sauveGarde (){
if (typeof(Storage) !== "undefined") {
// Store
localStorage.setItem("camStatus", camEtat);
localStorage.setItem("cons_interval", parseInt(cons_intv)/1000);
localStorage.setItem("gph_interval", parseInt(gph_intv)/1000);
localStorage.setItem("consf", consf);
//console.log("sauvegarde faite");
localStorage.setItem("loraStatus", loraEtat);
}
else {
console.log("Désolé, le navigateur que vous utiliser ne supporte pas le Web Storage...");
}
} 



      //x = e.data;
     /* if (typeof(Storage) !== "undefined") {
      // Store
      localStorage.setItem("pression", x);
      // Retrieve
      document.getElementById("result").innerHTML = localStorage.getItem("pression");
    } else {
      document.getElementById("result").innerHTML = "Sorry, your browser does not support Web Storage...";
    } */
  
     
  
     // Get current sensor readings when the page loads
  //window.addEventListener('DOMContentLoaded', ouverturePage);
  //window.addEventListener('load', ouverturePage);
  //window.addEventListener('readystatechange', ouverturePage);  
  
 
  
  
  // FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS 

  function dateHeure(){   // fonction pour renvoyer la date et l'heure actuelle
    var today = new Date();
    var date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = time+' '+date;
    return dateTime;
  }
  
  

  
  
  // Fonctions pour rendre le menu de la page index.html inteactif
    function mOver1(obj) {document.getElementById("m1").style.background = "#FFA07A";}
    function mOut1(obj) { document.getElementById("m1").style.background = "transparent";}
    function mOver2(obj) {document.getElementById("m2").style.background = "#FFA07A";}
    function mOut2(obj) { document.getElementById("m2").style.background = "transparent";}
    function mOver3(obj) {document.getElementById("m3").style.background = "#FFA07A"; }
    function mOut3(obj) {document.getElementById("m3").style.background = "transparent";}
    function mOver4(obj) {document.getElementById("m4").style.background = "#FFA07A";}
    function mOut4(obj) {document.getElementById("m4").style.background = "transparent";}
    function mOver5(obj) {document.getElementById("m5").style.background = "#FFA07A"; }
    function mOut5(obj) {document.getElementById("m5").style.background = "transparent"; }
 
    
 // Fonctions pour créer les liens vers les autres pages du menu   
// var myWindowIndex;
  var myWindowGraphe;
  var myWindowConsole;
  var myWindowHardware;
  var myWindowTele;
  
  /*  function menuIndex() {
      
      if ((!myWindowIndex)||(myWindowIndex.closed)) 
  
      {myWindowIndex= window.open("index.html","_blank", " width=screen.width, height=screen.height, menubar=no, directories=no, location=no, scrollbars=no, status =no");}
      else {myWindowIndex.focus();}
    }
  */
    function menuGraph() {
     
      if ((!myWindowGraphe)||(myWindowGraphe.closed)) 
      {myWindowGraphe= window.open("graphes.html","_blank", " width=1200px, height=800px,menubar=no, directories=no, location=no, scrollbars=no, status =no");}
      else {myWindowGraphe.focus(); } 
  
    }
    function menuConsole() {
      if ((!myWindowConsole)||(myWindowConsole.closed)) 
      {myWindowConsole = window.open("console.html","_blank", " width=1200px, height=800px,menubar=no, directories=no, location=no, scrollbars=no, status =no");}
      
      else {myWindowConsole.focus();}
    
    }
    function menuHardware() {
      if ((!myWindowHardware)||(myWindowHardware.closed)) 
      {myWindowHardware = window.open("controle.html","_blank", " width=1200px, height=800px, menubar=no, directories=no, location=no, scrollbars=no, status =no");}
      
      else {myWindowHardware.focus();}
    }
    function menuTele() { 
      if ((!myWindowTele)||(myWindowTele.closed)) 
    { myWindowTele = window.open("telecommandes.html","_blank", "width=1200px, height=800px, menubar=no, directories=no, location=no, scrollbars=no, status =no");}
    else {myWindowTele.focus();}
    }
/*
// Fonction pour Alerte à la fermuture de la page
  window.onbeforeunload = function(){ // Alerte à la fermuture de la page
  return "Any!"
}    
*/
  
// INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF INTF  
 
    if (!!window.EventSource) {
      var source = new EventSource('/events3');
  
      source.addEventListener('open', function(e) {
        console.log(dateHeure());
        console.log("Debut de la reception des donnees satellite ...");
      }, false);
    
      source.addEventListener('error', function(e) {
        if (e.target.readyState != EventSource.OPEN) {
          console.log(dateHeure());
          console.log("Reception des donnees satellite interrompue ...");
        }
    }, false);
    
    source.addEventListener('CAP_readings3', function(e) {
      var obj3 = JSON.parse(e.data);
       console.log(obj3);
      document.getElementById("var1").innerHTML =  Number(obj3.var1).toFixed(3);
      document.getElementById("var2").innerHTML =  Number(obj3.var4).toFixed(3);
      document.getElementById("var3").innerHTML =  Number(obj3.var6).toFixed(3);
      document.getElementById("var4").innerHTML =  Number(obj3.var21).toFixed(3);
      document.getElementById("var5").innerHTML =  Number(obj3.var22).toFixed(3);
      document.getElementById("var6").innerHTML =  Number(obj3.var23).toFixed(3);
      document.getElementById("var7").innerHTML =  Number(obj3.var18).toFixed(3);
      document.getElementById("var8").innerHTML =  Number(obj3.var19).toFixed(3);
      document.getElementById("var9").innerHTML =  Number(obj3.var20).toFixed(3);
      document.getElementById("var10").innerHTML =  Number(obj3.var24).toFixed(3);
      document.getElementById("var11").innerHTML =  Number(obj3.var25).toFixed(3);
      document.getElementById("var12").innerHTML =  Number(obj3.var26).toFixed(3);
      document.getElementById("var13").innerHTML =  Number(obj3.var30).toFixed(3);
      document.getElementById("var14").innerHTML =  Number(obj3.var31).toFixed(3);
      document.getElementById("var15").innerHTML =  Number(obj3.var32).toFixed(3);
      document.getElementById("var16").innerHTML =  Number(obj3.var11).toFixed(3);
      document.getElementById("var17").innerHTML =  Number(obj3.var12).toFixed(3);
      document.getElementById("var18").innerHTML =  Number(obj3.var13).toFixed(3);
      document.getElementById("var19").innerHTML =  Number(obj3.var8).toFixed(3);
      document.getElementById("var20").innerHTML =  Number(obj3.var9).toFixed(3);
      document.getElementById("var21").innerHTML =  Number(obj3.var10).toFixed(3);
   
      
    }, false);
  }
  
/*  
function fermePage() {
  if(window.confirm("Arréter et fermer toutes les pages de l'interface ?")) {
    myWindowResult =localStorage.getItem("result"); 
  var xhr = new XMLHttpRequest();
    xhr.open("GET", "/fermePage", true);
    xhr.send();
   window.close();
   myWindowConsole.close();
   myWindowGraphe.close();
   myWindowHardware.close();
   myWindowTele.close();
   myWindowResult.close();
  }
}

*/  
  

setInterval(function(){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/user", true);
  xhr.send();

},300000);