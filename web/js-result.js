var filetxt = "";
var consol_his=document.getElementById("console_box");
document.getElementById("console_").style.color = "black";
var consConf= localStorage.getItem("consf");  // var consConf="00000000000000";
document.getElementById("cmd_").innerHTML = (".").fontcolor("white");



// CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE CONSOLE 
if (!!window.EventSource) {

    var source = new EventSource('/events');
    
    source.addEventListener('open', function(e) {
      console.log(dateHeure());
      console.log("Debut de la reception des donnees satellite ...");
      document.getElementById("console_").innerHTML += (">> ").fontcolor("red");
      document.getElementById("console_").innerHTML +=dateHeure().fontcolor("red")+"\r\n"
      filetxt = filetxt + dateHeure()+"\r\n";
      document.getElementById("console_").innerHTML +="Debut de la reception des donnees satellite ...\r\n";
      filetxt = filetxt + "Debut de la reception des donnees satellite ...\r\n";
    }, false);
  
    source.addEventListener('error', function(e) {
      if (e.target.readyState != EventSource.OPEN) {
        console.log(dateHeure());
        console.log("Reception des donnees satellite interrompue ...");
        document.getElementById("console_").innerHTML += (">> ").fontcolor("red");
        document.getElementById("console_").innerHTML +=dateHeure().fontcolor("red")+"\r\n"
        filetxt = filetxt + dateHeure()+"\r\n";
        document.getElementById("console_").innerHTML +="Reception des donnees satellite interrompue ...\r\n";
        filetxt = filetxt + "Reception des donnees satellite interrompue ...\r\n";
      }
    }, false);
  
    
    source.addEventListener('CAP_readings', function(e) {
      
    // consConf =localStorage.getItem("consf"); 
    var obj = JSON.parse(e.data);

    consConf = obj.var51;
    
    localStorage.setItem("consf", consConf);
    //console.log(consConf);

      if(consConf!=="00000000000000")
       {
         console.log('%c%s','color: red; font-size: 12px', dateHeure());   //; font-weight:bold
         document.getElementById("console_").innerHTML += (">> ").fontcolor("red");
         document.getElementById("console_").innerHTML +=dateHeure().fontcolor("red")+"\r\n"
         filetxt = filetxt + dateHeure()+"\r\n";
     //console.log("CAP_readings", e.data);
       

        if (consConf.charAt(0)=='1') { 
        var etat = " ";
        switch (obj.var7) {
        case '1' :{etat = "bat_detect_failed_fault";} break;
        case '2' :{etat = "battery_detection";} break;
        case '3' :{etat = "charge_suspended";} break;
        case '4' :{etat = "precharge";} break;
        case '5' :{etat = "cc_cv-charge";} break;
        case '6' :{etat = "ntc_pause";} break;
        case '7' :{etat = "timer_term";} break;
        case '8' :{etat = "c_over_x_term";} break;
        case '9' :{etat = "max_charge_time_fault";} break;
        case '10' :{etat = "bat_missing_fault";} break;
        case '11' :{etat = "bat_short_fault";} break;
        case '0' :{etat = "unknown";} break;
        default: {etat = "unknown";}
        } 
      console.log('%cEnergie : %cVbat = %s V, Vin = %s V, Vout = %s V, Ibat = %s A, Iin = %s A, Tbat = %s °c, Etat de charge : %s.','color: blue; font-size: 12px',' ', Number(obj.var1).toFixed(3),Number(obj.var2).toFixed(3),Number(obj.var3).toFixed(3),Number(obj.var4).toFixed(3),Number(obj.var5).toFixed(3),Number(obj.var6).toFixed(3), etat );
      var titre = "Energie : ";
      filetxt = filetxt + "Energie : Vbat = "+Number(obj.var1).toFixed(3)+" V, Vin = "+Number(obj.var2).toFixed(3)+" V, Vout = "+Number(obj.var3).toFixed(3)+" V, Icharge = "+Number(obj.var4).toFixed(3)+" A, Iin = "+Number(obj.var5).toFixed(3)+" A, Tbat = "+Number(obj.var6).toFixed(3)+" °c, Etat de charge : "+etat+"\r\n";
     
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+"Vbat = "+Number(obj.var1).toFixed(3)+" V, Vin = "+Number(obj.var2).toFixed(3)+" V, Vout = "+Number(obj.var3).toFixed(3)+" V, Icharge = "+Number(obj.var4).toFixed(3)+" A, Iin = "+Number(obj.var5).toFixed(3)+" A, Tbat = "+Number(obj.var6).toFixed(3)+" °c, Etat de charge : "+etat+"\r\n";  
      //console.log('Vbat = %s V, Vin = %s V, Vout = %s V, Ibat = %s A, Iin = %s A, Tbat = %s °c, , Etat de charge : %s.',Number(obj.var1).toFixed(3),Number(obj.var2).toFixed(3),Number(obj.var3).toFixed(3),Number(obj.var4).toFixed(3),Number(obj.var5).toFixed(3),Number(obj.var6).toFixed(3), obj.var7);
      }
      if (consConf.charAt(1)=='1') {
      console.log('%cTempérature (°c): %cT = %s.', 'color: blue; font-size: 12px', '', Number(obj.var8).toFixed(3)); 
      filetxt = filetxt + "Température (°c): T = "+Number(obj.var8).toFixed(3)+"\r\n";
      var titre = "Température (°c) : "
      document.getElementById("console_").innerHTML += titre.fontcolor("blue")+"T = "+Number(obj.var8).toFixed(3)+"\r\n";
    }
      //console.log('T = %s.', Number(obj.var8).toFixed(3)); }
  
      if (consConf.charAt(2)=='1') {
      console.log('%cAltitude (m): %cAl = %s.' , 'color: blue; font-size: 12px','',Number(obj.var9).toFixed(3)); 
      filetxt = filetxt + "Altitude (m) : Al = "+Number(obj.var9).toFixed(3)+"\r\n";
      var titre = "Altitude (m): ";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+ "Al = "+Number(obj.var9).toFixed(3)+"\r\n";
      //console.log('Al = %s.', Number(obj.var9).toFixed(3)); }
    }
      if (consConf.charAt(3)=='1') {
      console.log('%cPréssion (Pa) : %cPr = %s.', 'color: blue; font-size: 12px','', Number(obj.var10).toFixed(3)); 
      filetxt = filetxt + "Préssion (Pa): Pr = "+Number(obj.var10).toFixed(3)+"\r\n";
      var titre = "Préssion (Pa): "; 
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+"Pr = "+Number(obj.var10).toFixed(3)+"\r\n"; 
    }
      
  
      if (consConf.charAt(4)=='1') {
      console.log('%cVecteur Euler (°): %cRoulis = %s, Tangage = %s, Lacet = %s.', 'color: blue; font-size: 12px',' ', Number(obj.var11).toFixed(3), Number(obj.var12).toFixed(3), Number(obj.var13).toFixed(3)); 
      filetxt = filetxt + "Vecteur Euler (°): Roulis = "+Number(obj.var11).toFixed(3)+", Tangage = "+Number(obj.var12).toFixed(3)+", Lacet = "+Number(obj.var13).toFixed(3)+"\r\n";
      var titre = "Vecteur Euler (°) : ";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+"Roulis = "+Number(obj.var11).toFixed(3)+", Tangage = "+Number(obj.var12).toFixed(3)+", Lacet = "+Number(obj.var13).toFixed(3)+"\r\n";
    }
      //console.log('Roulis = %s, Tangage = %s, Lacet = %s.', Number(obj.var11).toFixed(3), Number(obj.var12).toFixed(3), Number(obj.var13).toFixed(3)); }
  
      if (consConf.charAt(5)=='1') {
      console.log('%Quaternion : %cW = %s, X = %s, Y = %s, Z = %s.', 'color: blue; font-size: 12px','',Number(obj.var14).toFixed(3), Number(obj.var15).toFixed(3),Number(obj.var16).toFixed(3), Number(obj.var17).toFixed(3)); 
      filetxt = filetxt + "Quaternion : W = "+Number(obj.var14).toFixed(3)+", X = "+Number(obj.var15).toFixed(3)+", Y = "+Number(obj.var16).toFixed(3)+", Z = "+Number(obj.var17).toFixed(3)+"\r\n";
      var titre = "Quaternion : ";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+ "W = "+Number(obj.var14).toFixed(3)+", X = "+Number(obj.var15).toFixed(3)+", Y = "+Number(obj.var16).toFixed(3)+", Z = "+Number(obj.var17).toFixed(3)+"\r\n";
    }
      //console.log('W = %s, X = %s, Y = %s, Z = %s.', Number(obj.var14).toFixed(3), Number(obj.var15).toFixed(3),Number(obj.var16).toFixed(3), Number(obj.var17).toFixed(3)); }
    
      if (consConf.charAt(6)=='1') {
      console.log('%cVitesse Angulaire (rad/s): %cX = %s, y = %s, z = %s.', 'color: blue; font-size: 12px','',Number(obj.var18).toFixed(3), Number(obj.var19).toFixed(3), Number(obj.var20).toFixed(3)); 
      filetxt = filetxt + "Vitesse Angulaire (rad/s): X = "+Number(obj.var18).toFixed(3)+", Y = "+Number(obj.var19).toFixed(3)+", Z = "+Number(obj.var20).toFixed(3)+"\r\n";
      var titre = "Vitesse Angulaire (rad/s) : ";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+ "X = "+Number(obj.var18).toFixed(3)+", Y = "+Number(obj.var19).toFixed(3)+", Z = "+Number(obj.var20).toFixed(3)+"\r\n";
    }
      // console.log('X = %s, y = %s, z = %s.', Number(obj.var18).toFixed(3), Number(obj.var19).toFixed(3), Number(obj.var20).toFixed(3)); }
    
      if (consConf.charAt(7)=='1') {
      console.log('%cAccelération (m/s²): %cX = %s, Y = %s, Z = %s.', 'color: blue; font-size: 12px','',Number(obj.var21).toFixed(3), Number(obj.var22).toFixed(3), Number(obj.var23).toFixed(3)); 
      filetxt = filetxt + "Accelération (m/s²): X = "+Number(obj.var21).toFixed(3)+", Y = "+Number(obj.var22).toFixed(3)+", Z = "+Number(obj.var23).toFixed(3)+"\r\n";
      var titre = "Accelération (m/s²) : ";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+"X = "+Number(obj.var21).toFixed(3)+", Y = "+Number(obj.var22).toFixed(3)+", Z = "+Number(obj.var23).toFixed(3)+"\r\n";  
    }
      //console.log('X = %s, Y = %s, Z = %s.', Number(obj.var21).toFixed(3), Number(obj.var22).toFixed(3), Number(obj.var23).toFixed(3)); }
  
      if (consConf.charAt(8)=='1') {
      console.log('%cChamps Magnétique (uT): %cX = %s, Y = %s, Z = %s.', 'color: blue; font-size: 12px','',Number(obj.var24).toFixed(3), Number(obj.var25).toFixed(3), Number(obj.var26).toFixed(3)); 
      filetxt = filetxt + "Champs Magnétique (uT): X = "+Number(obj.var24).toFixed(3)+", Y = "+Number(obj.var25).toFixed(3)+", Z = "+Number(obj.var26).toFixed(3)+"\r\n";  
      var titre = "Champs Magnétique (uT) : ";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+"X = "+Number(obj.var24).toFixed(3)+", Y = "+Number(obj.var25).toFixed(3)+", Z = "+Number(obj.var26).toFixed(3)+"\r\n"; 
    }
      //console.log('X = %s, Y = %s, Z = %s.', Number(obj.var24).toFixed(3), Number(obj.var25).toFixed(3), Number(obj.var26).toFixed(3)); }
  
      if (consConf.charAt(9)=='1') {
      console.log('%cAccelération Linéaire (m/s²) : %cX = %s, Y = %s, Z = %s.', 'color: blue; font-size: 12px','', Number(obj.var27).toFixed(3), Number(obj.var28).toFixed(3), Number(obj.var29).toFixed(3)); 
      filetxt = filetxt + "Accelération Linéaire (m/s²) : X = "+Number(obj.var27).toFixed(3)+", Y = "+Number(obj.var28).toFixed(3)+", Z = "+Number(obj.var29).toFixed(3)+"\r\n";  
      var titre = "Accelération Linéaire (m/s²) : ";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+ "X = "+Number(obj.var27).toFixed(3)+", Y = "+Number(obj.var28).toFixed(3)+", Z = "+Number(obj.var29).toFixed(3)+"\r\n"; 
      }
      //console.log('X = %s, Y = %s, Z = %s.', Number(obj.var27).toFixed(3), Number(obj.var28).toFixed(3), Number(obj.var29).toFixed(3)); }
  
      if (consConf.charAt(10)=='1') {
      console.log('%cVecteur Gravité (m/s²): %cX = %s, Y = %s, Z = %s.', 'color: blue; font-size: 12px','',Number(obj.var30).toFixed(3), Number(obj.var31).toFixed(3), Number(obj.var32).toFixed(3)); 
      filetxt = filetxt + "Vecteur Gravité (m/s²): X = "+Number(obj.var30).toFixed(3)+", Y = "+Number(obj.var31).toFixed(3)+", Z = "+Number(obj.var32).toFixed(3)+"\r\n";   
      var titre = "Vecteur Gravité (m/s²) : ";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+ "X = "+Number(obj.var30).toFixed(3)+", Y = "+Number(obj.var31).toFixed(3)+", Z = "+Number(obj.var32).toFixed(3)+"\r\n";
    }
     // console.log('X = %s, Y = %s, Z = %s.', Number(obj.var30).toFixed(3), Number(obj.var31).toFixed(3), Number(obj.var32).toFixed(3)); }
  
      if (consConf.charAt(11)=='1') {
      console.log('%cLuminance : %c+X = %s, -X = %s, +Y = %s, -Y = %s, Z = %s.', 'color: blue; font-size: 12px','',Number(obj.var33).toFixed(3), Number(obj.var34).toFixed(3), Number(obj.var35).toFixed(3), Number(obj.var36).toFixed(3), Number(obj.var37).toFixed(3)); 
      filetxt = filetxt + "Luminance : +X = "+Number(obj.var33).toFixed(3)+", -X = "+Number(obj.var34).toFixed(3)+", +Y = "+Number(obj.var35).toFixed(3)+", -Y = "+Number(obj.var36).toFixed(3)+", Z = "+Number(obj.var37).toFixed(3)+"\r\n";    
      var titre = "Luminance : ";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+ "+X = "+Number(obj.var33).toFixed(3)+", -X = "+Number(obj.var34).toFixed(3)+", +Y = "+Number(obj.var35).toFixed(3)+", -Y = "+Number(obj.var36).toFixed(3)+", Z = "+Number(obj.var37).toFixed(3)+"\r\n"; 
    }
      //console.log('+X = %s, -X = %s, +Y = %s, -Y = %s, Z = %s.', Number(obj.var33).toFixed(3), Number(obj.var34).toFixed(3), Number(obj.var35).toFixed(3), Number(obj.var36).toFixed(3), Number(obj.var37).toFixed(3)); }
    
      if (consConf.charAt(12)=='1') {
      console.log('%cLocalisation GNSS : %cUTC = %s, Latitude = %s, Longitude = %s, Nb Satellites = %s.', 'color: blue; font-size: 12px','',obj.var38, obj.var39, obj.var40, obj.var41); 
      filetxt = filetxt + "Localisation GNSS : UTC = "+obj.var38+", Latitude = "+obj.var39+", Longitude = "+obj.var40+", Nb Satellites = "+obj.var41+"\r\n";    
      var titre = "Localisation GNSS : ";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue")+"UTC = "+obj.var38+", Latitude = "+obj.var39+", Longitude = "+obj.var40+", Nb Satellites = "+obj.var41+"\r\n";
    }
      //console.log('UTC = %s, Latitude = %s, Longitude = %s, Nb Satellites = %s.', obj.var38, obj.var39, obj.var40, obj.var41); }
    
      if (consConf.charAt(13)=='1') {
      console.log('%cGNSS - Trame NMEA :', 'color: blue; font-size: 12px'); 
      console.log('%s%s%s%s%s%s%s%s%s', obj.var42, obj.var43, obj.var44, obj.var45, obj.var46, obj.var47, obj.var48, obj.var49, obj.var50);
      filetxt = filetxt + "GNSS- Trame NMEA : "+obj.var42+obj.var43+obj.var44+obj.var45+obj.var46+obj.var47+obj.var48+obj.var49+obj.var50+"\r\n";   
      var titre = "GNSS- Trame NMEA : \r\n";
      document.getElementById("console_").innerHTML +=titre.fontcolor("blue") +obj.var42+obj.var43+obj.var44+obj.var45+obj.var46+obj.var47+obj.var48+obj.var49+obj.var50+"\r\n";  
    }
    filetxt = filetxt+"\r\n"; 
    document.getElementById("console_").innerHTML +="\r\n";
    if (def==1) {consol_his.scrollTop=consol_his.scrollHeight;}

       }
    }, false);
  }
  
  
  // FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS 

  function dateHeure(){   // fonction pour renvoyer la date et l'heure actuelle
    var today = new Date();
    var date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = time+' '+date;
    return dateTime;
  }
  
         
 
// Fonction pour alerter à la fermeture de la page 
window.onbeforeunload = function(){ 
return "Any"
}    




function saveDataToFile() {

  //var userInput = "Essai numero 1";

  var blob = new Blob([filetxt], { type: "text/plain;charset=utf-8" });
  saveAs(blob, "INISAT_console"+dateHeure()+".txt");
}

var def=1;

function defAct(element) {
        if(element.checked){ def=1; }
        else {def=0; }

    console.log(def);
}

function effResult() {
   
    document.getElementById("console_").innerHTML =(">>").fontcolor("red")+"\r\n";
}


/// event AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST 
if (!!window.EventSource) {

  var source = new EventSource('/events4');
  
  source.addEventListener('TEST_readings', function(e) {
    var obj2 = JSON.parse(e.data);
    
    document.getElementById("console_").innerHTML += (">> ").fontcolor("red");
    document.getElementById("console_").innerHTML +=dateHeure().fontcolor("red")+"\r\n";
    filetxt = filetxt + dateHeure()+"\r\n";
    document.getElementById("console_").innerHTML += "\r\n"+("... Auto-Test Result ... ").fontcolor("red")+"\r\n";
    filetxt = filetxt + "\r\n"+"... Auto-Test Result ... "+"\r\n";

    document.getElementById("console_").innerHTML +=obj2.var1+"\r\n";
    filetxt = filetxt +obj2.var1+"\r\n";
    document.getElementById("console_").innerHTML +=obj2.var2+"\r\n";
    filetxt = filetxt +obj2.var2+"\r\n";
    document.getElementById("console_").innerHTML +="INISAT_IP_ADDRESS : "+obj2.var3+"\r\n";
    filetxt = filetxt + "INISAT_IP_ADDRESS : "+obj2.var3+"\r\n";
    if (obj2.var4.charAt(0)=='1') { var x = "PING_CAMERA_SUCCESS (at 192.168.4.183), PING_AVERAGE_TIME : "+obj2.var4.substr(1)+" ms";  }
    else { var x = "PING_CAMERA_FAILED (at 192.168.4.183) / or Camera Off";  }
    document.getElementById("console_").innerHTML +=x+"\r\n";
    filetxt = filetxt + x+"\r\n";
    document.getElementById("console_").innerHTML +="LORA_Signal Power (dBm) : "+obj2.var5+"\r\n";
    filetxt = filetxt +"LORA_Signal Power (dBm) : "+ obj2.var5+"\r\n";
    document.getElementById("console_").innerHTML +="LORA_Spreading Factor : "+obj2.var6+"\r\n";
    filetxt = filetxt + "LORA_Spreading Factor : "+obj2.var6+"\r\n";
    if(obj2.var6=='0') {
    document.getElementById("console_").innerHTML += "... LORA Module ERROR ..."+"\r\n";
    filetxt = filetxt + "... LORA Module ERROR ..."+"\r\n";
    } 
    document.getElementById("console_").innerHTML +="LORA_Signal Bandwidth (Hz): "+obj2.var7+"\r\n";
    filetxt = filetxt + "LORA_Signal Bandwidth (Hz): "+obj2.var7+"\r\n";
    document.getElementById("console_").innerHTML +="LORA_Signal Frequency (MHz): "+obj2.var8+"\r\n";
    filetxt = filetxt + "LORA_Signal Frequency (MHz): "+obj2.var8+"\r\n";
    document.getElementById("console_").innerHTML +="LORA_Coding Rate (4/x): "+obj2.var9+"\r\n";
    filetxt = filetxt + "LORA_Coding Rate (4/x): "+ obj2.var9+"\r\n";
    document.getElementById("console_").innerHTML +="LORA_Preamble Length : "+obj2.var10+"\r\n";
    filetxt = filetxt +"LORA_Preamble Length : "+obj2.var10+"\r\n";
    document.getElementById("console_").innerHTML +=obj2.var11+"\r\n";
    filetxt = filetxt + obj2.var11+"\r\n";
    document.getElementById("console_").innerHTML +=obj2.var12+"\r\n";
    filetxt = filetxt + obj2.var12+"\r\n";
    document.getElementById("console_").innerHTML +=obj2.var13+"\r\n";
    filetxt = filetxt + obj2.var13+"\r\n";
    document.getElementById("console_").innerHTML +=obj2.var14+"\r\n"+"\r\n";
    filetxt = filetxt + obj2.var14+"\r\n"+"\r\n";




    if (def==1) {consol_his.scrollTop=consol_his.scrollHeight;}
    //filetxt = filetxt + obj2+"\r\n"; 
  }, false);
}  


setInterval(function(){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/user", true);
  xhr.send();

},300000);


function validateFormCMD(){
  var commande = document.forms["myFormCMD"]["CMD"].value;
  //commande = commande.substr(4);
  commande = commande.trim();
  commande = commande.toLowerCase();
  
 
 
  consConf =localStorage.getItem("consf"); 
  var consfg =[];
  for (var i=0; i<consConf.length; i++) {
    consfg [i] = consConf.charAt(i);
  }

/*
  console.log(commande);
  console.log(consConf);
  console.log(consfg);
*/

  var flag = 0;

  
 /*    
  document.getElementById("cmd_").innerHTML = (".").fontcolor("white");
  setTimeout(function(){document.getElementById("cmd_").innerHTML = ("Commande envoyée !").fontcolor("green"); },100);
  document.forms["myFormCMD"]["CMD"].value = ("   ");
  setTimeout(function(){document.forms["myFormCMD"]["CMD"].value = (" >> ") },100);
 */ 
  document.getElementById("console_").innerHTML +=dateHeure().fontcolor("red")+"\r\n"
  filetxt = filetxt + dateHeure()+"\r\n";
  document.getElementById("console_").innerHTML +=(" >> ").fontcolor("green")+(commande).fontcolor("green") + "\r\n"; 
  filetxt = filetxt + " >> " + commande +"\r\n";

  switch (commande) {
  case 'epson' :{ consfg [0]= '1'; flag = 1;} break;
  case 'epsoff' :{consfg [0]= '0'; flag = 1;} break;
  case 'mplon' :{consfg [1]='1'; consfg [2]= '1'; consfg [3]= '1'; flag = 1;} break;
  case 'mploff' :{consfg [1]='0'; consfg [2]= '0'; consfg [3]= '0'; flag = 1;} break;
  case 'tempon' :{consfg [1]= '1'; flag = 1;} break;
  case 'tempoff' :{consfg [1]= '0'; flag = 1;} break;
  case 'alton' :{consfg [2]= '1'; flag = 1;} break;
  case 'altoff' :{consfg [2]= '0'; flag = 1;} break;
  case 'preson' :{consfg [3]='1'; flag = 1;} break;
  case 'presoff' :{consfg [3]='0'; flag = 1;} break;
  case 'bnoon' :{consfg [4]= '1';consfg [5]= '1';consfg [6]= '1';consfg [7]= '1';consfg [8]= '1';consfg [9]= '1';consfg [10]= '1';flag = 1;} break;
  case 'bnooff' :{consfg [4]= '0';consfg [5]= '0';consfg [6]= '0';consfg [7]= '0';consfg [8]= '0';consfg [9]= '0';consfg [10]= '0';flag = 1;} break;
  case 'euleron' :{consfg [4]='1'; flag = 1;} break;
  case 'euleroff' :{consfg [4]='0'; flag = 1;} break;
  case 'quaton' :{consfg [5]= '1'; flag = 1;} break;
  case 'quatoff' :{consfg [5]= '0'; flag = 1;} break;
  case 'vangon' :{consfg [6]= '1'; flag = 1;} break;
  case 'vangoff' :{consfg [6]= '0'; flag = 1;} break;
  case 'accon' :{consfg [7]= '1'; flag = 1;} break;
  case 'accoff' :{consfg [7]='0'; flag = 1;} break;
  case 'magon' :{consfg [8]= '1'; flag = 1;} break;
  case 'magoff' :{consfg [8]= '0'; flag = 1;} break;
  case 'acclnon' :{consfg [9]= '1'; flag = 1;} break;
  case 'acclnoff' :{consfg [9]= '0'; flag = 1;} break;
  case 'gravon' :{consfg [10]='1'; flag = 1;} break;
  case 'gravoff' :{consfg [10]='0'; flag = 1;} break;
  case 'lumion' :{consfg [11]= '1'; flag = 1;} break;
  case 'lumioff' :{consfg [11]= '0'; flag = 1;} break;
  case 'locon' :{consfg [12]= '1'; flag = 1;} break;
  case 'locoff' :{consfg [12]= '0'; flag = 1;} break;
  case 'nmeaon' :{consfg [13]='1'; flag = 1;} break;
  case 'nmeaoff' :{consfg [13]='0'; flag = 1;} break;
  case 'allon' : {consfg=['1','1','1','1','1','1','1','1','1','1','1','1','1','1']; flag = 1;} break;
  case 'alloff' :{consfg=['0','0','0','0','0','0','0','0','0','0','0','0','0','0']; flag = 1;} break;
  

  case 'loraon' : {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;  
      document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";   
      filetxt = filetxt + obj + "\r\n";
      }}
    xhr.open("GET", "/LoraON", true); 
    xhr.send();
    localStorage.setItem("loraStatus", 1);
  } flag = 2; break;
  
  case 'loraoff' : {

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;  
      document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n"; 
      filetxt = filetxt + obj + "\r\n";  
      }}
    xhr.open("GET", "/LoraOFF", true) 
    xhr.send();
    localStorage.setItem("loraStatus", 0);
  } flag = 2; break;

  case 'lorastate' : {

  if (localStorage.getItem("loraStatus")==1) {document.getElementById("console_").innerHTML += ("Etat LORA est : ON").fontcolor("green")+ "\r\n"; filetxt = filetxt +"Etat LORA est : ON"+ "\r\n"; }
  else { document.getElementById("console_").innerHTML += ("Etat LORA est : OFF").fontcolor("green")+ "\r\n"; filetxt = filetxt +"Etat LORA est : OFF"+ "\r\n"; }
  } flag = 2; break;


 case 'camon' : {

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var obj = this.responseText; 
    document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
    filetxt = filetxt + obj + "\r\n";
  }}
  xhr.open("GET", "/CamON", true); 
  xhr.send();
  localStorage.setItem("camStatus", 1); 
 } flag = 2; break;

case 'camoff': { 

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    var obj = this.responseText;   
    document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
    filetxt = filetxt + obj + "\r\n";
    }}
  xhr.open("GET", "/CamOFF", true) ;
  xhr.send();
  localStorage.setItem("camStatus", 0); 
} flag = 2; break;

case 'camstate' : { 

  if (localStorage.getItem("camStatus")==1) {document.getElementById("console_").innerHTML += ("Etat CAM est : ON").fontcolor("green")+ "\r\n"; filetxt = filetxt +"Etat CAM est : ON"+ "\r\n";}
  else {document.getElementById("console_").innerHTML += ("Etat CAM est : OFF").fontcolor("green")+ "\r\n"; filetxt = filetxt +"Etat CAM est : OFF"+ "\r\n";}
  } flag = 2; break;

  case 'camcapture' : { 
    if (localStorage.getItem("camStatus")==1) { var myWindow = window.open("http://192.168.4.183/capture","Capture", "width=640px, height=480px, menubar=no, directories=no, location=no, scrollbars=no, status =no, status = no");}
    else { var myWindow = window.open("camoff.html","Cam Off", "width=1200px, height=800px,menubar=no, directories=no, location=no, scrollbars=no, status =no, status = no");}
  } flag = 2; break;

  case 'camstream' : { 
    if (localStorage.getItem("camStatus")==1) { var myWindow = window.open("http://192.168.4.183:81/stream","Stream", "width=640px, height=480px, menubar=no, directories=no, location=no, scrollbars=no, status =no, status = no" );}
  else { var myWindow = window.open("camoff.html","Cam Off", " width=1200px, height=800px, menubar=no, directories=no, location=no, scrollbars=no, status =no, status = no");}
  } flag = 2; break;

  case 'autotest' : { 
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
      filetxt = filetxt + obj + "\r\n";
      }}
    xhr.open("GET", "/autoTest", true);
    xhr.send();
    
  } flag = 2; break;

  case 'scons' :{ saveDataToFile(); flag = 2;} break;


  case 'dmagon' :{
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
      document.getElementById("console_").innerHTML += ("Veuillez attendre la fin ..").fontcolor("green")+ "\r\n";  
      filetxt = filetxt + obj + "\r\n";
      filetxt = filetxt + "Veuillez attendre la fin .." + "\r\n";
      }}
    xhr.open("GET", "/demag", true);
    xhr.send();
  } flag = 2; break;

  case 'magt1' :{
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
      filetxt = filetxt + obj + "\r\n";
      }}
    xhr.open("GET", "/tst1", true);
    xhr.send();
  } flag = 2; break;

  case 'magt2' :{
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
      filetxt = filetxt + obj + "\r\n";
      }}
    xhr.open("GET", "/tst2", true);
    xhr.send();
  } flag = 2; break;

  case 'magt3' :{
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
      filetxt = filetxt + obj + "\r\n";
      }}
    xhr.open("GET", "/tst3", true);
    xhr.send();
  } flag = 2; break;

  case 'magt4' :{
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
      filetxt = filetxt + obj + "\r\n";
      }}
    xhr.open("GET", "/tst4", true);
    xhr.send();
  } flag = 2; break;

  case 'stpmgt' :{
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n"; 
      document.getElementById("console_").innerHTML += ("Veuillez attendre la fin ..").fontcolor("green")+ "\r\n";  
      filetxt = filetxt + obj + "\r\n";
      filetxt = filetxt + "Veuillez attendre la fin .." + "\r\n";
      }}
    xhr.open("GET", "/tststp", true);
    xhr.send();
  } flag = 2; break;

  case 'help' :{ 
    var htext = ""; 
    htext = htext +	"	acclnOff :	Désactiver la supervision de l'Accelération Linéaire 	"	+ "\r\n"; 
    htext = htext +	"	acclnOn :	Activer la supervision de l'Accelération Linéaire	"	+ "\r\n"; 
    htext = htext +	"	accOff :	Désactiver la supervision de l'Accelération	"	+ "\r\n"; 
    htext = htext +	"	accOn :	Activer la supervision de l'Accelération	"	+ "\r\n"; 
    htext = htext +	"	allOff :	Désactiver la supervision de l'ensemble des paramètres	"	+ "\r\n"; 
    htext = htext +	"	allOn :	Activer la supervision de  l'ensemble des paramètres	"	+ "\r\n"; 
    htext = htext +	"	altOff :	Désactiver la supervision de l'Altitude	"	+ "\r\n"; 
    htext = htext +	"	altOn :	Activer la supervision de l'Altitude	"	+ "\r\n"; 
    htext = htext +	"	autoTest :	Lancer un Autotest	"	+ "\r\n"; 
    htext = htext +	"	bnoOff :	Désactiver la supervision de l'ensemble des paramètres renvoyés par le BNO	"	+ "\r\n"; 
    htext = htext +	"	bnoOn :	Activer la supervision de  l'ensemble des paramètres renvoyés par le BNO	"	+ "\r\n"; 
    htext = htext +	"	camCapture :	Prendre une capture avec la Caméra	"	+ "\r\n"; 
    htext = htext +	"	camOff :	Désactiver la Caméra	"	+ "\r\n"; 
    htext = htext +	"	camOn :	Activer la Caméra	"	+ "\r\n"; 
    htext = htext +	"	camState :	Afficher l'état de la Caméra	"	+ "\r\n"; 
    htext = htext +	"	camStream :	Démarrer un stream avec la Caméra	"	+ "\r\n"; 
    htext = htext +	"	dmagOn :	Lancer une démagnétisation des magnétocoupleurs	"	+ "\r\n"; 
    htext = htext +	"	epsOff :	Désactiver la supervision de l'ensemble des paramètres de la carte EPS	"	+ "\r\n"; 
    htext = htext +	"	epsOn :	Activer la supervision de  l'ensemble des paramètres de la carte EPS	"	+ "\r\n"; 
    htext = htext +	"	eulerOff :	Désactiver la supervision de Vecteur d'Euler	"	+ "\r\n"; 
    htext = htext +	"	eulerOn :	Activer la supervision de Vecteur d'Euler	"	+ "\r\n"; 
    htext = htext +	"	gravOff :	Désactiver la supervision de Vecteur Gravité	"	+ "\r\n"; 
    htext = htext +	"	gravOn :	Activer la supervision de Vecteur Gravité	"	+ "\r\n"; 
    htext = htext +	"	help :	Afficher la liste des commandes existantes et leurs explications	"	+ "\r\n"; 
    htext = htext +	"	locOff :	Activer la supervision de la localisation GNSS	"	+ "\r\n"; 
    htext = htext +	"	locOn :	Désactiver la supervision de la localisation GNSS	"	+ "\r\n"; 
    htext = htext +	"	loraOff :	Désactiver la liaison LORA	"	+ "\r\n"; 
    htext = htext +	"	loraOn :	Activer la liaison LORA	"	+ "\r\n"; 
    htext = htext +	"	loraState :	Afficher l'état de la liaison LORA	"	+ "\r\n"; 
    htext = htext +	"	lumiOff :	Désactiver la supervision de la Luminance	"	+ "\r\n"; 
    htext = htext +	"	lumiOn :	Activer la supervision de la Luminance	"	+ "\r\n"; 
    htext = htext +	"	magOff :	Désactiver la supervision de Champs Magnétique	"	+ "\r\n"; 
    htext = htext +	"	magOn :	Activer la supervision de Champs Magnétique	"	+ "\r\n"; 
    htext = htext +	"	magT1 : 	Lancer le test rotation boussole par magnétocoupleurs N°1 "	+ "\r\n"; 
    htext = htext +	"	magT2 : 	Lancer le test rotation boussole par magnétocoupleurs N°2 "	+ "\r\n"; 
    htext = htext +	"	magT3 : 	Lancer le test rotation boussole par magnétocoupleurs N°3 "	+ "\r\n"; 
    htext = htext +	"	magT4 : 	Lancer le test rotation boussole par magnétocoupleurs N°4 "	+ "\r\n"; 
    htext = htext +	"	mgRot+angle :	Démarrer une rotation du satellite via les magnétocoupleurs, exp : mgRot+10, mgRot+-15 (en °)	"	+ "\r\n"; 
    htext = htext +	"	mplOff :	Désactiver la supervision de l'ensemble des paramètres renvoyés par le MPL	"	+ "\r\n"; 
    htext = htext +	"	mplOn :	Activer la supervision de  l'ensemble des paramètres renvoyés par le MPL	"	+ "\r\n"; 
    htext = htext +	"	nmeaOff :	Désactiver la supervision de la trame GNSS-NMEA	"	+ "\r\n"; 
    htext = htext +	"	nmeaOn :	Activer la supervision de la trame GNSS-NMEA	"	+ "\r\n"; 
    htext = htext +	"	presOff :	Désactiver la supervision de la Préssion	"	+ "\r\n"; 
    htext = htext +	"	presOn :	Activer la supervision de la Préssion	"	+ "\r\n"; 
    htext = htext +	"	quatOff :	Désactiver la supervision du quaternion	"	+ "\r\n"; 
    htext = htext +	"	quatOn :	Activer la supervision du quaternion	"	+ "\r\n"; 
    htext = htext +	"	riRot+sens+vitesse :	Démarrer une rotation de la roue à inertie, exp : riRot+a+40  (en %)	"	+ "\r\n"; 
    htext = htext +	"	sCons :	Sauvegarder toutes les données de la console dans un fichier .txt	"	+ "\r\n"; 
    htext = htext +	"	stpmgT : 	Arrêter le test magnétocoupleurs en cours 	"	+ "\r\n"; 
    htext = htext +	"	tCons+période :	Modifier la periode de réception des données sur la console, exp tCons+10  (en secondes)	"	+ "\r\n"; 
    htext = htext +	"	tempOff :	Désactiver la supervision de la Température	"	+ "\r\n"; 
    htext = htext +	"	tempOn :	Activer la supervision de la Température	"	+ "\r\n"; 
    htext = htext +	"	vangOff :	Désactiver la supervision de la Vitesse Angulaire	"	+ "\r\n"; 
    htext = htext +	"	vangOn :	Activer la supervision de la Vitesse Angulaire	"	+ "\r\n"; 
    
    htext = htext + "\r\n" +	"	Remarque : la saisie des commandes n'est pas sensible à la casse.	"	+ "\r\n"; 
    
    document.getElementById("console_").innerHTML += (htext).fontcolor("burlywood")+ "\r\n";  
   filetxt = filetxt + htext + "\r\n";
htext = "";
    flag = 2;} break;


  default: {
    var commd = commande.substring(0,5);
    switch (commd) {
      case 'tcons' :{ 

  var tt = commande.substring(5,6);
  if (tt!='+') {flag = 0; break; }

  var tt2 = commande.substring(6)
  if (isNaN(tt2)) {
    document.getElementById("console_").innerHTML +=  ("Veuillez choisir une periode entre 5 et 3600 secondes !").fontcolor("red")+"\r\n";
    filetxt = filetxt + ("Veuillez choisir une periode entre 5 et 3600 secondes !")+"\r\n"; 
    flag = 2; break; }

        var T_cons = Number(commande.substring(6)); 
        console.log(T_cons);
       

    if ((T_cons<5) || (T_cons>3600)) {
    document.getElementById("console_").innerHTML +=  ("Veuillez choisir une periode entre 5 et 3600 secondes !").fontcolor("red")+"\r\n";
    filetxt = filetxt + ("Veuillez choisir une periode entre 5 et 3600 secondes !")+"\r\n"; 
  }
    else {
    localStorage.setItem("interval", T_cons);
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
      filetxt = filetxt + obj + "\r\n";
      }}
      xhr.open("GET", "/t_console?choix="+T_cons, true);
      xhr.send();
    } flag = 2;} break;


      case 'rirot' :{ 

        var tt = commande.substring(5,6);
        if (tt!='+') {flag = 0; break; }

        var tt2 = commande.substring(7,8);
        if (tt2!='+') {flag = 0; break; }

        var tt3 = commande.substring(8)
        if (isNaN(tt3)) {
        document.getElementById("console_").innerHTML +=  ("Veuillez choisir une valeur entre 0 et 100 % !").fontcolor("red")+"\r\n";
        filetxt = filetxt + ("Veuillez choisir une valeur entre 0 et 100 % !")+"\r\n";
        flag = 2; break; }

        var sens = commande.substring(6,7);
        var speed = Number(commande.substring(8));
        
        //console.log(speed);
        //console.log(sens);
        
        if ((speed<0) || (speed>100)) {
          document.getElementById("console_").innerHTML +=  ("Veuillez choisir une valeur entre 0 et 100 % !").fontcolor("red")+"\r\n";
          filetxt = filetxt + ("Veuillez choisir une valeur entre 0 et 100 % !")+"\r\n";
          flag = 2; break; 
        }  

        if ((sens!='a') && (sens!='h')) {
          document.getElementById("console_").innerHTML +=  ("Veuillez choisir A ou H pour le Sens de rotation !").fontcolor("red")+"\r\n";
          filetxt = filetxt + ("Veuillez choisir A ou H pour le Sens de rotation !")+"\r\n"; 
        } 
        else {
          var xhr = new XMLHttpRequest();
          xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
            var obj = this.responseText;
            document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
            filetxt = filetxt + obj + "\r\n";
            }}
          xhr.open("GET", "/roue?choix="+(sens+speed), true);
          xhr.send();
        }

        flag = 2;} break;
      case 'mgrot' :{ 

        var tt = commande.substring(5,6);
        if (tt!='+') {flag = 0; break; }

        var coup = commande.substring(6); 
        if (isNaN(coup)) {
          document.getElementById("console_").innerHTML +=  ("Veuillez choisir une valeur entre -30 et 30° ! (et != 0)").fontcolor("red")+"\r\n";
          filetxt = filetxt + ("Veuillez choisir une valeur entre -30 et 30° ! (et != 0)")+"\r\n";
          flag = 2; break; }

          var A_coup= Number(commande.substring(6));
        
        if ((A_coup<-30) || (A_coup>30) || (A_coup==0)) {
          document.getElementById("console_").innerHTML +=  ("Veuillez choisir une valeur entre -30 et 30° ! (et != 0)").fontcolor("red")+"\r\n";
          filetxt = filetxt + ("Veuillez choisir une valeur entre -30 et 30° ! (et != 0)")+"\r\n"; 
        }
        else {
          var xhr = new XMLHttpRequest();
          xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
            var obj = this.responseText;
            document.getElementById("console_").innerHTML += (obj).fontcolor("green")+ "\r\n";  
            filetxt = filetxt + obj + "\r\n";
            }}
          xhr.open("GET", "/ang_couple?choix="+A_coup, true);
          xhr.send();
        }
        flag = 2; } break; 
        
      
      


      default: {flag = 0;} break;
    }
    
    } break;


  
  } 

  consConf=consfg[0]+consfg[1]+consfg[2]+consfg[3]+consfg[4]+consfg[5]+consfg[6]+consfg[7]+consfg[8]+consfg[9]+consfg[10]+consfg[11]+consfg[12]+consfg[13];


  if (flag==0) {
    document.getElementById("console_").innerHTML +=  ("Commande Non Existante").fontcolor("red")+"\r\n";
    filetxt = filetxt + ("Commande Non Existante")+"\r\n";
    document.getElementById("cmd_").innerHTML = (".").fontcolor("white");
    setTimeout(function(){document.getElementById("cmd_").innerHTML = ("Commande Non Existante, Veuillez Consulter la Commande \" HELP. \"").fontcolor("red"); },100);
    setTimeout(function(){document.forms["myFormCMD"]["CMD"].value = (" ") },100);

    
  }

  if (flag==1) {

    localStorage.setItem("consf", consConf);
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText; 
      if(obj=="OKOK") {document.getElementById("console_").innerHTML += (commande).fontcolor("green")+ (" Exécutée ..").fontcolor("green")+"\r\n";  }
      filetxt = filetxt + (commande).fontcolor("green")+ " Exécutée .." + "\r\n";
      }}
    xhr.open("GET", "/cons_config?choix="+consConf, true);
    xhr.send();

    document.getElementById("cmd_").innerHTML = (".").fontcolor("white");
    setTimeout(function(){document.getElementById("cmd_").innerHTML = ("Commande envoyée !").fontcolor("green"); },100);
    setTimeout(function(){document.forms["myFormCMD"]["CMD"].value = (" ") },100);
}

if (flag==2) {
  document.getElementById("cmd_").innerHTML = (".").fontcolor("white");
  setTimeout(function(){document.getElementById("cmd_").innerHTML = ("Commande envoyée !").fontcolor("green"); },100);
  setTimeout(function(){document.forms["myFormCMD"]["CMD"].value = (" ") },100);
  
}

if (def==1) {consol_his.scrollTop=consol_his.scrollHeight;}

}

// EVENT FIN DEMAGNETISATION EVENT FIN DEMAGNETISATION EVENT FIN DEMAGNETISATION EVENT FIN DEMAGNETISATION EVENT FIN DEMAGNETISATION EVENT FIN DEMAGNETISATION 

if (!!window.EventSource) {
  var source = new EventSource('/events5');


source.addEventListener('fct_fin', function(e) {
  var obj = e.data;
  if (obj=="A"){

    document.getElementById("console_").innerHTML += ("Démagnetisation finie").fontcolor("brown")+ "\r\n";  
   filetxt = filetxt + " .. Démagnetisation finie" + "\r\n";

              }

  if (obj=="B"){

    document.getElementById("console_").innerHTML += ("Test fini").fontcolor("brown")+ "\r\n";  
    filetxt = filetxt + " .. Test fini" + "\r\n";
              }
}, false);
}