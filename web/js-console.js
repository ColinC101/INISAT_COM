
  
  // FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS 
  function dateHeure(){   // fonction pour renvoyer la date et l'heure actuelle
    var today = new Date();
    var date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = time+' '+date;
    return dateTime;
  }
  
  // Fonction pour lire la periode et la configuration déja configurée et afficher correctement ce qui corréspond
  var consConf="00000000000000";
  var intv = 5;
  window.onload = function() { // same as window.addEventListener('load', (event) => {
    intv = localStorage.getItem("cons_interval")
    document.getElementById("intv_").innerHTML = ("Période actuelle : "+intv+" secondes").fontcolor("green");
    document.forms["myForm0"]["Cons_Temps"].value = intv;
    consConf =localStorage.getItem("consf"); 
    var ele=document.getElementsByName('consol_conf');  
    for(var i=0; i<ele.length; i++){  
        if (consConf.charAt(i)=='1') {ele[i].checked=true;}
        else {ele[i].checked=false;}  
    }

  };
  
  
  // Fonction à exécuter à la : validation du formulaire 0, temps de rafraichissement de la console sur la page console.html
  
  function validateForm0() {
  var  T_cons = document.forms["myForm0"]["Cons_Temps"].value;
    if ((T_cons<5) || (T_cons>3600)) {
      console.log('%c%s','color: red; font-size: 12px ', dateHeure());
      console.log('%cVeuillez choisir une periode entre 5 et 3600 secondes !',"color:orange;font-size: 12px; font-weight:bold");
      document.getElementById("intv_").innerHTML = ("rien").fontcolor("transparent");
      setTimeout(function(){document.getElementById("intv_").innerHTML = ("Veuillez choisir une periode entre 1 et 3600 secondes !").fontcolor("red"); },200); }
    else {
      console.log('%c%s','color: red; font-size: 12px', dateHeure());
    console.log('%cLa periode choisie est : %s secondes',"color:green;font-size: 12px; font-weight:bold",T_cons);
    localStorage.setItem("interval", T_cons);
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("intv_").innerHTML = (".").fontcolor("white");
      setTimeout(function(){document.getElementById("intv_").innerHTML = (obj).fontcolor("green"); },100);
      }}
      xhr.open("GET", "/t_console?choix="+T_cons, true);
      xhr.send();
    }
  }
  
  
  // Fonction pour valider le formulaire consForm en checkbox sur la page console.html
 
  function validateconsForm() {
    var M_cons="";
  if (document.getElementById("eps_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("tp_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("al_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("prss_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("eul_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("quat_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("vang_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("acc_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("mag_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("accl_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("vgrv_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("lum_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("gnss_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
  if (document.getElementById("nmoa_").checked) {M_cons=M_cons+"1";} 
  else {M_cons=M_cons+"0";} 
  
    console.log(M_cons);
    consConf = M_cons;
    localStorage.setItem("consf", consConf);
    var xhr = new XMLHttpRequest();
      xhr.open("GET", "/cons_config?choix="+M_cons, true);
      xhr.send();
      menuResult();

  }
  var myWindowResult;
  function menuResult() {
    if ((!myWindowResult)||(myWindowResult.closed)) 
    {myWindowResult = window.open("result.html","_blank", " width=1200px, height=800px, menubar=no, directories=no, location=no, scrollbars=no, status =no");
    localStorage.setItem("result", myWindowResult);}
    
    else {myWindowResult.focus();}
  }


  // fonction pour les button de select Tout et effacer tous les chechboxs de la page console
  function selects(){  
    var ele=document.getElementsByName('consol_conf');  
    for(var i=0; i<ele.length; i++){  
        if(ele[i].type=='checkbox')  
            ele[i].checked=true;  
    }  
}  
function deSelect(){  
    var ele=document.getElementsByName('consol_conf');  
    for(var i=0; i<ele.length; i++){  
        if(ele[i].type=='checkbox')  
            ele[i].checked=false;  
          
    }  
}             
 
/*
// Fonction pour alerter à la fermeture de la page 
window.onbeforeunload = function(){ 
return "Any"
}    
*/

  // fonction npour envoyer une requet afin d'effectuer un autotest
  function autoTest() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("auto_").innerHTML = (".").fontcolor("white");
      setTimeout(function(){document.getElementById("auto_").innerHTML = (obj).fontcolor("green"); },100);
      }}
    xhr.open("GET", "/autoTest", true);
    xhr.send();
    menuResult();
   }


   // fonction pour envoyer un indication si le client est toujours connecté sur cette page, tt les 5 min ici 
   setInterval(function(){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/user", true);
    xhr.send();
  
  },300000);