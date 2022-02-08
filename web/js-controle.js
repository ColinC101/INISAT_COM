// FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS 

  function dateHeure(){   // fonction pour renvoyer la date et l'heure actuelle
    var today = new Date();
    var date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = time+' '+date;
    return dateTime;
  }
  
  
  function toggleCheckbox1(element) {   // button pour activer/desactiver la liaison LORA
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("lora_").innerHTML = (obj).fontcolor("green");
      }}
    if(element.checked){ xhr.open("GET", "/LoraON", true); localStorage.setItem("loraStatus", 1);}
    else { xhr.open("GET", "/LoraOFF", true); localStorage.setItem("loraStatus", 0); }
    xhr.send();
  }
  
  function toggleCheckbox2(element) {  // button pour activer/desactiver la teseERA
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("camera_").innerHTML = (obj).fontcolor("green");
      }}
    if(element.checked){ xhr.open("GET", "/CamON", true); localStorage.setItem("camStatus", 1);}
    else { xhr.open("GET", "/CamOFF", true); localStorage.setItem("camStatus", 0); }
    console.log(localStorage.getItem("camStatus"));
    xhr.send();
  }
  

  function toggleCheckbox3(element) {  // button pour activer/desactiver le capteur 9-axes (BNO)  --- fonctionne pas actuellement
    var xhr = new XMLHttpRequest();
    if(element.checked){ xhr.open("GET", "/Cap9ON", true); }
    else { xhr.open("GET", "/Cap9OFF", true) }
    xhr.send();
  }

    window.onload = function() { // same as window.addEventListener('load', (event) => {
 
    document.getElementById("lora_").innerHTML = (".").fontcolor("white");
    document.getElementById("camera_").innerHTML = (".").fontcolor("white");


  };
