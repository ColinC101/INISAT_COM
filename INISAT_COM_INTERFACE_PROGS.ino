#include <Arduino.h>
#include <WiFi.h>
#include <WiFiGeneric.h>
#include <ESP32Ping.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <Arduino_JSON.h>
#include "SPIFFS.h"
// Libraries for LoRa
#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <math.h>
#include <WiFiUdp.h> // pour la transmission des trames UDP

//#include <esp_task_wdt.h>
//#define WDT_TIMEOUT 1800

// define the pins used by the LORA transceiver module**************************************************************************************************************
#define SCK 5
#define MISO 19
#define MOSI 27
#define SS 18
#define RST 14
#define DIO0 26
#define LORA_LED 2 // led temoins on/off transmission lora
#define BAND 866E6 // 866E6 for Europede

#define COMM_LED 4    // led temoins configuration WIFI et SPIFFS OK
#define CAM_STATUT 12 // Port pour la commande Hard de la camera (ON/OFF)

//---------------------------------------------------------------------------------------------------------------------------------------------------

// String cmd =""; // commande pour l'echgange UART avec le processeur calculateur
int user = 0;            // utilisateur connecte ou non a l'interface inisat sur un navigateur
String Temp_String = ""; // String pour stocker les donnees recus du microcontrolleur principal
char inChar;
// int miseAjour = 0;
int flag = 0; // variable flag de qui indique qu'il y a au moins un parametre qui a ete selectionne dans la trame console config, et donc on envoi un Z.
// donnees pour initialiser le wifi********************************************************************************************************************************
const char *ssid = "INISAT 210703"; // "INISAT 210704";  211101;
const char *password = "123456789";
int chan = 1;
int ssid_hidden = 0;
int max_connection = 4;
int wifiOk = 0;
int loraOk = 0;
int spiffsOk = 0;
IPAddress INISAT_IP(192, 168, 4, 1);

String var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21, var22, var23, var24, var25;
String var26, var27, var28, var29, var30, var31, var32, var33, var34, var35, var36, var37, var38, var39, var40, var41, var42, var43, var44, var45, var46, var47, var48, var49, var50;
float var21B, var22B, var23B, var24B, var25B, var26B, var27B, var28B, var29B, var30B, var31B, var32B;

JSONVar readings;  // variable utilise dans les fonction : getLocReadings pour faire le stockage et la conversion vers JSON
JSONVar readings2; // variable utilise dans les fonction : getLocReadings pour faire le stockage et la conversion vers JSON
JSONVar readings3; // variable utilise dans les fonction : getLocReadings pour faire le stockage et la conversion vers JSON

// JSONVar INTF_readings; // variable utilise dans les fonction : getLocReadings pour faire le stockage et la conversion vers JSON
JSONVar Index_init; // variable pour envoyer les donnee d'initialisation (etat cam, interval, config console) a l'ouverture de la page index.
JSONVar AUTOtEST;   // variable pour envoyer les donnee d'initialisation (etat cam, interval, config console) a l'ouverture de la page index.

// Variables a utilises dans LORA Tx*******************************************************************************************************************************
int readingID = 1;
int counter = 0;
// String LoRaMessage = "";

// variables utilisees dans la partie controle*************************************************************************************************
unsigned long startTime;
unsigned long console_start;
unsigned long graph_start;
unsigned long interface_start;
unsigned long user_start;
unsigned long lora_start;
unsigned long modeGnss_start;

// unsigned long startTimeIntf;
int INTV = 1000; // intervalle de mise a jours des donnees a partir de la carte OBC
int console_intv = 5000;
int graph_intv = 5000;
int interface_intv = 60000; // 1 min
int lora_intv = 90000;      // 1min30s
int user_intv = 330000;     // 5min30
int modeGnss_intv = 2000;   // 2 sec

int aff_cons = 0;
int aff_graph = 0;
int aff_interface = 0;
int aff_lora = 0;
int affCons_ex = 0;
int affGraph_ex = 0;
int affInt_ex = 0;
int affLora_ex = 0;

int angRotCoup; // valeur en degre pour fire tourner le magnetocoupleur
int demag = 0;
String Roue_Inertie; // variable pour stocker la commande recue pour la roue d'inertie : sens+vitesse
int LoraStatus = 0;  // Commande soft de la Liaison LORA, (0 transmission LORA off au demarrage, 1 On au demarrage)
int CamStatus = 0;   // Commande soft de la camera (0 camera off au demarrage, 1 On au demarrage)
// int Cap9Axes = 1;
String consConfig = "00000000000000";
String saveConfig = "00000000000000";
char chart1 = '0';
char chart2 = '0';
char chart3 = '0';
char chart4 = '0';
char chart5 = '0';
char chart6 = '0';
int autotest = 0;
int autoTesting = 0;

// Variables pour la ROUE A INERTIE ou Magnetocoupleur X  ************************
const int pwmPin = 23;  // 23 corresponds to GPIO23
const int sensPin = 25; // corresponds to GPIO25
// setting PWM properties
const int freq = 5000;
const int ChannelX = 4;
const int resolution = 8;

// Variables pour le Magnetocoupleur Y ************************
const int pwmPinY = 32;  // 32 corresponds to GPIO32
const int sensPinY = 33; // 33 corresponds to GPIO33
const int freqY = 5000;
const int ChannelY = 5;
const int resolutionY = 8;
int testmg = 0;
String dmagFin = "N";
String testfin = "N";

int modeGnss = 0; // variable utilise pour lancer le mode Releve de trajectoire GNSS
int modeGnss_ex = 0;
int aff_modeGnss = 0;

// Create AsyncWebServer object on port 80 *************************************************************************************************************************
AsyncWebServer server(80);

// Create an Event Source on /events ********************************************************************************************************************************
AsyncEventSource events("/events");   // event pour la console
AsyncEventSource events2("/events2"); // event pour graphes
AsyncEventSource events3("/events3"); // event pour interface
AsyncEventSource events4("/events4"); // event pour AUTOTEST
AsyncEventSource events5("/events5"); // event pour FIN de la DEMAGNETISATION

// Variables pour utiliser le protocole UDP <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
char packetBuffer[32];
// char  ReplyBuffer[];       // a string to send back
String ReplyBuffer;
int packetSize = 0;
int len = 0;
String valeurs[14]; // tableau utilise pour la transmission des trames UDP
int udp_Ex = 0;     // variable pour l'activation ou desactivation de la liaison UDP
unsigned int localPort = 9991;
WiFiUDP Udp; // Creation of wifi Udp instance
//***************************************************************************

// LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA
// Initialize LoRa module
void startLoRA()
{
  pinMode(SS, OUTPUT);
  // SPI LoRa pins
  SPI.begin(SCK, MISO, MOSI, SS);
  // setup LoRa transceiver module
  digitalWrite(SS, LOW); //<<<<<<<<<<<< selectionner SPI LORA
  LoRa.setPins(SS, RST, DIO0);
  while (!LoRa.begin(BAND) && counter < 10)
  {
    Serial.print(".");
    counter++;
    delay(500);
  }
  if (counter == 10)
  {
    Serial.println("Starting LoRa failed!");
  }
  else
  {
    LoRa.setSyncWord(0x5F);

    // valeurs par defaut :
    LoRa.setTxPower(17); // 17dBm
    LoRa.setSpreadingFactor(7);
    LoRa.setSignalBandwidth(125E3);
    LoRa.setCodingRate4(5); // 4/5
    LoRa.setPreambleLength(8);
    LoRa.disableCrc(); // LoRa.enableCrc();

    // https://github.com/sandeepmistry/arduino-LoRa/blob/master/API.md

    Serial.println("LoRa Initialisation OK ...");
    Serial.println("(TxPower : 17dBm, SpreadingFactor : 7, SignalBandwidth : 125E3, CodingRate : 4/5, PreambleLength : 8, disableCrc) ");
    loraOk = 1;
  }
}
// LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA LORA

// SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS
//  initialisation du systeme SPIFFS pour la sauvegarde des fichiers dans la carte
void initSPIFFS()
{
  if (!SPIFFS.begin())
  {
    Serial.println("An error has occurred while mounting SPIFFS");
    return;
  }

  Serial.println("SPIFFS mounted successfully");
  spiffsOk = 1;
}
// SPIFFS SPIFFSSPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS SPIFFS

// fonction de sauvegarde des variables dans un fichier .txt*******************************************************************************************************

void file_SPIFFS()
{

  File file = SPIFFS.open("/Trajectoire_GNSS.txt", "a");
  if (!file)
  {
    // File not found
    Serial.println("Failed to open test file for save");
    return;
  }
  else
  {
    file.print(var39);
    file.print(" , ");
    file.println(var40);
    file.close();
    Serial.println(" Data receved and saved on Trajectoire_GNSS.txt ... ");
  }
}

// Initialisation du WiFi WIFI WIFIWIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI

/*#################
void initWiFi() {

// Setting the ESP as an access point
Serial.println("Configuration WIFI en Access Point (AP)…"); //####################
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.mode(WIFI_AP); //####################
 // WiFi.softAP(ssid, password);
 //WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
 WiFi.softAP(ssid,password,chan, ssid_hidden, max_connection); //####################
 WiFi.setTxPower(WIFI_POWER_19_5dBm);  //####################

  IPAddress IP = WiFi.softAPIP();
  delay(200);


wifi_power_t tx_power;
tx_power=WiFi.getTxPower();
int m = WiFi.getMode();

  if ((m==2)&& (tx_power==78)&&(IP ==INISAT_IP)){
  Serial.print("Configuration effectuee, AP IP address : ");
  Serial.println(IP);
  Serial.println("WIFI Tx Power : 19.5dBm");
  //Serial.println("(78: 19.5dBm, 76: 19dBm, 74: 18.5dBm, 68: 17dBm, 60: 15dBm, 52: 13dBm, 44: 11dBm, 34: 8.5dBm, 28: 7dBm, 20: 5dBm, 8:  2dBm, -4: -1dBm)");

  wifiOk =1;
  }
  else {
    Serial.print("Intialisation WIFI non effectuee correctement !!!! ");
    return;
    }


}
#################*/
// WIFI WIFIWIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI WIFI

// fonction pour transmettre les donnes par LORA*******************************************************************************************************************
// les donnees sont transmises par trames LORA de 3 variables (+ un identifiant au debut)
// pour assurer la stabilite du recepteur
/*
void sendReadings() {

 digitalWrite(SS, LOW); //<<<<<<<<<<<< selectionner SPI LORA
 LoRaMessage = String(1) + "/" + String(var1) + "&" + String(var1) + "#" + String(var1);
 //Send LoRa packet to receiver
 LoRa.beginPacket();
 LoRa.print(LoRaMessage);
 LoRa.endPacket();
 Serial.print("Envoi de la trame LORA N°: ");
 Serial.println(readingID);
 Serial.print(LoRaMessage);
 delay(200);

 LoRaMessage = String(2) + "/" + String(var1) + "&" + String(var1) + "#" + String(var1);
 LoRa.beginPacket();
 LoRa.print(LoRaMessage);
 LoRa.endPacket();
 Serial.print(LoRaMessage);
 delay(200);

 LoRaMessage = String(3) + "/" +  String(var1) + "&" + String(var1) + "#" + String(var1);
 LoRa.beginPacket();
 LoRa.print(LoRaMessage);
 LoRa.endPacket();
 Serial.print(LoRaMessage);
 delay(200);

 LoRaMessage = String(4) + "/" +  String(var1) + "&" + String(var1) + "#" + String(var1);
 //Send LoRa packet to receiver
 LoRa.beginPacket();
 LoRa.print(LoRaMessage);
 LoRa.endPacket();
 Serial.print(LoRaMessage);
 delay(200);

 LoRaMessage = String(5) + "/" + String(var1) + "&" + String(var1) + "#" + String(var1);
 //Send LoRa packet to receiver
 LoRa.beginPacket();
 LoRa.print(LoRaMessage);
 LoRa.endPacket();
 Serial.print(LoRaMessage);
 delay(200);

LoRaMessage = String(6) + "/" +  String(var1) + "&" + String(var1) + "#" + String(var1);
 //Send LoRa packet to receiver
 LoRa.beginPacket();
 LoRa.print(LoRaMessage);
 LoRa.endPacket();
 Serial.print(LoRaMessage);
 delay(200);

 LoRaMessage = String(7) + "/" + String(var1) + "&" + String(var1) + "#" + String(var1);
 //Send LoRa packet to receiver
 LoRa.beginPacket();
 LoRa.print(LoRaMessage);
 LoRa.endPacket();
 Serial.println(LoRaMessage);
 delay(200);
 readingID++;
}
*/
// fonction pour convertir les valeurs transmises par les capteur, les changer en format JSON, en 1 packet ,****************************************************
// pour pouvoir le transmettre a la page web avec la fonction sendEvent ()
String Readings()
{ // pour la console
  readings["var1"] = var1;
  readings["var2"] = var2;
  readings["var3"] = var3;
  readings["var4"] = var4;
  readings["var5"] = var5;
  readings["var6"] = var6;
  readings["var7"] = var7;
  readings["var8"] = var8;
  readings["var9"] = var9;
  readings["var10"] = var10;
  readings["var11"] = var11;
  readings["var12"] = var12;
  readings["var13"] = var13;
  readings["var14"] = var14;
  readings["var15"] = var15;
  readings["var16"] = var16;
  readings["var17"] = var17;
  readings["var18"] = var18;
  readings["var19"] = var19;
  readings["var20"] = var20;
  readings["var21"] = var21;
  readings["var22"] = var22;
  readings["var23"] = var23;
  readings["var24"] = var24;
  readings["var25"] = var25;
  readings["var26"] = var26;
  readings["var27"] = var27;
  readings["var28"] = var28;
  readings["var29"] = var29;
  readings["var30"] = var30;
  readings["var31"] = var31;
  readings["var32"] = var32;
  readings["var33"] = var33;
  readings["var34"] = var34;
  readings["var35"] = var35;
  readings["var36"] = var36;
  readings["var37"] = var37;
  readings["var38"] = var38;
  readings["var39"] = var39;
  readings["var40"] = var40;
  readings["var41"] = var41;
  readings["var42"] = var42;
  readings["var43"] = var43;
  readings["var44"] = var44;
  readings["var45"] = var45;
  readings["var46"] = var46;
  readings["var47"] = var47;
  readings["var48"] = var48;
  readings["var49"] = var49;
  readings["var50"] = var50;
  readings["var51"] = consConfig;
  String CAPString = JSON.stringify(readings);
  return CAPString;
}

String Readings2()
{ // pour l'interface et graphes
  readings2["var1"] = var1;
  readings2["var2"] = "";
  readings2["var3"] = "";
  readings2["var4"] = var4;
  readings2["var5"] = "";
  readings2["var6"] = var6;
  readings2["var7"] = "";
  readings2["var8"] = var8;
  readings2["var9"] = var9;
  readings2["var10"] = var10;
  readings2["var11"] = var11;
  readings2["var12"] = var12;
  readings2["var13"] = var13;
  readings2["var14"] = var14;
  readings2["var15"] = var15;
  readings2["var16"] = var16;
  readings2["var17"] = var17;
  readings2["var18"] = var18;
  readings2["var19"] = var19;
  readings2["var20"] = var20;
  readings2["var21"] = var21;
  readings2["var22"] = var22;
  readings2["var23"] = var23;
  readings2["var24"] = var24;
  readings2["var25"] = var25;
  readings2["var26"] = var26;
  readings2["var27"] = var27;
  readings2["var28"] = var28;
  readings2["var29"] = var29;
  readings2["var30"] = var30;
  readings2["var31"] = var31;
  readings2["var32"] = var32;
  readings2["var33"] = var33;
  readings2["var34"] = var34;
  readings2["var35"] = var35;
  readings2["var36"] = var36;
  readings2["var37"] = var37;

  String CAPString = JSON.stringify(readings2);
  return CAPString;
}

String Readings3()
{ // pour lora
  readings3["var1"] = var1;
  //  readings3["var2"] = "";
  //  readings3["var3"] = "";
  readings3["var4"] = var4;
  //  readings3["var5"] = "";
  readings3["var6"] = var6;
  readings3["var7"] = var7;
  readings3["var8"] = var8;
  readings3["var9"] = var9;
  readings3["var10"] = var10;
  readings3["var11"] = var11;
  readings3["var12"] = var12;
  readings3["var13"] = var13;
  readings3["var14"] = var14;
  readings3["var15"] = var15;
  readings3["var16"] = var16;
  readings3["var17"] = var17;
  readings3["var18"] = var18;
  readings3["var19"] = var19;
  readings3["var20"] = var20;
  readings3["var21"] = var21;
  readings3["var22"] = var22;
  readings3["var23"] = var23;
  readings3["var24"] = var24;
  readings3["var25"] = var25;
  readings3["var26"] = var26;
  //  readings3["var27"] = var27;
  //  readings3["var28"] = var28;
  //  readings3["var29"] = var29;
  readings3["var30"] = var30;
  readings3["var31"] = var31;
  readings3["var32"] = var32;
  readings3["var33"] = var33;
  readings3["var34"] = var34;
  readings3["var35"] = var35;
  readings3["var36"] = var36;
  readings3["var37"] = var37;
  readings3["var38"] = var38;
  readings3["var39"] = var39;
  readings3["var40"] = var40;
  readings3["var41"] = var41;
  String CAPString = JSON.stringify(readings3);
  return CAPString;
}
// fonction pour transmettre les valeurs des capteur a la page web via des evennements*****************************************************************************
void sendEventCons()
{
  events.send(Readings().c_str(), "CAP_readings", millis());
  Serial.println("event CAP_readings envoye");
}

void sendEventGraph()
{
  events2.send(Readings2().c_str(), "CAP_readings2", millis());
  Serial.println("event CAP_readings2 envoye");
}

void sendEventIntf()
{
  delay(1000);
  events3.send(Readings2().c_str(), "CAP_readings3", millis());
  Serial.println("event CAP_readings3 envoye");
}

// processeurs pour lire les etats actuelles des partie controle et affocher le code HTML correctement a l'ouverture des pages**************************************
String processor(const String &var)
{
  // Serial.println(var);
  if (var == "ETATLORA")
  {
    String buttons = "";
    if (LoraStatus == 1)
    {
      buttons = "<label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox1(this)\" id=\"Lora\" checked ><span class=\"slider\"></span></label>";
    }
    else
    {
      buttons = "<label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox1(this)\" id=\"Lora\" ><span class=\"slider\"></span></label>";
    }
    // Serial.println(buttons);
    return buttons;
  }

  if (var == "ETATCAM")
  {
    String buttons = "";
    if (CamStatus == 1)
    {
      buttons = "<label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox2(this)\" id=\"Cam\" checked ><span class=\"slider\"></span></label>";
    }
    else
    {
      buttons = "<label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox2(this)\" id=\"Cam\" ><span class=\"slider\"></span></label>";
    }
    // Serial.println(buttons);
    return buttons;
  }
  /*
    if(var == "ETATCAP9"){
      String buttons ="";
      if(Cap9Axes == 1){
      buttons ="<label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox3(this)\" id=\"Cap9\" checked ><span class=\"slider\"></span></label>";
    }
    else {
     buttons ="<label class=\"switch\"><input type=\"checkbox\" onchange=\"toggleCheckbox3(this)\" id=\"Cap9\" ><span class=\"slider\"></span></label>";

    }
    // Serial.println(buttons);
      return buttons;
    }
   */

  if (var == "MODEGNSS")
  {
    String buttons = "";
    if (modeGnss == 0)
    {
      buttons = "<input type=\"button\" class=\"button1\" value=\"Démarrer\" id=\"traj-on\" onclick=\"trajOn()\"> <input type=\"button\" class=\"button1\" value=\"Arrêter\" id=\"traj-off\" onclick=\"trajOff()\" style=\"background-color:rgb(124, 124, 124); cursor:none; \" disabled> <br> <a href=\"Trajectoire_GNSS.txt\" download=\"Trajectoire_GNSS.txt\"><input type=\"button\" class=\"button0\" value=\"Télécharger\" id=\"traj-save\" onclick=\"trajSave()\" > </a> <p><span id = \"trajectoire_\"></span></p>";
    }
    else
    {
      if (modeGnss == 1)
      {

        buttons = "<input type=\"button\" class=\"button1\" value=\"Démarrer\" id=\"traj-on\" onclick=\"trajOn()\" style=\"background-color:rgb(124, 124, 124); cursor:none;\" disabled> <input type=\"button\" class=\"button1\" value=\"Arrêter\" id=\"traj-off\" onclick=\"trajOff()\"> <br> <a href=\"Trajectoire_GNSS.txt\" download=\"Trajectoire_GNSS.txt\"><input type=\"button\" class=\"button0\" value=\"Télécharger\" id=\"traj-save\" onclick=\"trajSave()\" style=\"background-color:rgb(124, 124, 124); cursor:none; \" disabled> </a> <p><span id = \"trajectoire_\"></span></p>";
      }

      else
      {
        buttons = "<input type=\"button\" class=\"button1\" value=\"Démarrer\" id=\"traj-on\" onclick=\"trajOn()\" style=\"background-color:rgb(124, 124, 124); cursor:none; \" disabled> <input type=\"button\" class=\"button1\" value=\"Arrêter\" id=\"traj-off\" onclick=\"trajOff()\" style=\"background-color:rgb(124, 124, 124); cursor:none;\" disabled> <br> <a href=\"Trajectoire_GNSS.txt\" download=\"Trajectoire_GNSS.txt\"><input type=\"button\" class=\"button0\" value=\"Télécharger\" id=\"traj-save\" onclick=\"trajSave()\" ></a> <p><span id = \"trajectoire_\"></span></p>";
      }
    }
    // Serial.println(buttons);
    return buttons;
  }
  return String();
}
//// FONCTION -------------------------------------------------
String WIFIpowerRead()
{
  int m = WiFi.getTxPower();
  String x;
  switch (m)
  {
  case 78:
    x = "WIFI_POWER_19_5dBm";
    break;
  case 76:
    x = "WIFI_POWER_19dBm";
    break;
  case 74:
    x = "WIFI_POWER_18_5dBm";
    break;
  case 68:
    x = "WIFI_POWER_17dBm";
    break;
  case 60:
    x = "WIFI_POWER_15dBm";
    break;
  case 52:
    x = "WIFI_POWER_13dBm";
    break;
  case 44:
    x = "WIFI_POWER_11dBm";
    break;
  case 34:
    x = "WIFI_POWER_8_5dBm";
    break;
  case 28:
    x = "WIFI_POWER_7dBm";
    break;
  case 20:
    x = "WIFI_POWER_5dBm";
    break;
  case 8:
    x = "WIFI_POWER_2dBm";
    break;
  case -4:
    x = "WIFI_POWER_-1dBm";
    break;

  default:
    x = "No data";
    break;
  }

  return x;
}

String WIFImodeRead()
{
  int m = WiFi.getMode();
  String x;
  switch (m)
  {
  case 0:
    x = "WIFI_MODE_OFF";
    break;
  case 1:
    x = "WIFI_MODE_STA";
    break;
  case 2:
    x = "WIFI_MODE_AP";
    break;
  case 3:
    x = "WIFI_MODE_AP_STA";
    break;

  default:
    x = "No data";
    break;
  }

  return x;
}

String pingCamera()
{
  bool success;
  IPAddress ipcam(192, 168, 4, 183);
  String x;

  success = Ping.ping(ipcam);
  if (!success)
  {
    x = "0";
  }
  else
  {
    x = "1" + String(Ping.averageTime());
  }
  return x;
}
//*********************************************************************
void serialSend()
{
  // Serial.println("*******************dans sendSerial");
  /* Serial.print("user=");Serial.println(user);
      Serial.print("aff_interface=");Serial.println(aff_interface);*/
  if (((user == 1) || (LoraStatus == 1) || (udp_Ex == 1)) && (autoTesting == 0))
  {
    /*    Serial.println("********************dans user==1");
        Serial.print("user=");Serial.println(user);
        Serial.print("aff_interface=");Serial.println(aff_interface);*/

    if (((aff_cons == 1) && (consConfig.charAt(0) == '1')) || ((aff_graph == 1) && ((chart1 == 'k') || (chart2 == 'k') || (chart3 == 'k') || (chart4 == 'k') || (chart5 == 'k') || (chart6 == 'k'))) || ((aff_interface == 1) && (user == 1)) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('B');
      flag = 1;
      Serial.print('B');
    } // EPS
    if (((aff_cons == 1) && (consConfig.charAt(1) == '1')) || ((aff_graph == 1) && ((chart1 == 'h') || (chart2 == 'h') || (chart3 == 'h') || (chart4 == 'h') || (chart5 == 'h') || (chart6 == 'h'))) || ((aff_interface == 1) && (user == 1)) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('C');
      flag = 1;
      Serial.print('C');
    } // TEMPERATURE
    if (((aff_cons == 1) && (consConfig.charAt(2) == '1')) || ((aff_graph == 1) && ((chart1 == 'i') || (chart2 == 'i') || (chart3 == 'i') || (chart4 == 'i') || (chart5 == 'i') || (chart6 == 'i'))) || ((aff_interface == 1) && (user == 1)) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('D');
      flag = 1;
      Serial.print('D');
    } // ALTITUDE
    if (((aff_cons == 1) && (consConfig.charAt(3) == '1')) || ((aff_graph == 1) && ((chart1 == 'j') || (chart2 == 'j') || (chart3 == 'j') || (chart4 == 'j') || (chart5 == 'j') || (chart6 == 'j'))) || ((aff_interface == 1) && (user == 1)) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('E');
      flag = 1;
      Serial.print('E');
    } // PRESSION
    if (((aff_cons == 1) && (consConfig.charAt(4) == '1')) || ((aff_graph == 1) && ((chart1 == 'a') || (chart2 == 'a') || (chart3 == 'a') || (chart4 == 'a') || (chart5 == 'a') || (chart6 == 'a'))) || ((aff_interface == 1) && (user == 1)) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('F');
      flag = 1;
      Serial.print('F');
    } // VECTEUR EULER
    if (((aff_cons == 1) && (consConfig.charAt(5) == '1')) || ((aff_graph == 1) && ((chart1 == 'b') || (chart2 == 'b') || (chart3 == 'b') || (chart4 == 'b') || (chart5 == 'b') || (chart6 == 'b'))) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('G');
      flag = 1;
      Serial.print('G');
    } // QUATERNION
    if (((aff_cons == 1) && (consConfig.charAt(6) == '1')) || ((aff_graph == 1) && ((chart1 == 'c') || (chart2 == 'c') || (chart3 == 'c') || (chart4 == 'c') || (chart5 == 'c') || (chart6 == 'c'))) || ((aff_interface == 1) && (user == 1)) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('H');
      flag = 1;
      Serial.print('H');
    } // Vitesse Angulaire
    if (((aff_cons == 1) && (consConfig.charAt(7) == '1')) || ((aff_graph == 1) && ((chart1 == 'd') || (chart2 == 'd') || (chart3 == 'd') || (chart4 == 'd') || (chart5 == 'd') || (chart6 == 'd'))) || ((aff_interface == 1) && (user == 1)) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('I');
      flag = 1;
      Serial.print('I');
    } // ACCELERATION
    if (((aff_cons == 1) && (consConfig.charAt(8) == '1')) || ((aff_graph == 1) && ((chart1 == 'e') || (chart2 == 'e') || (chart3 == 'e') || (chart4 == 'e') || (chart5 == 'e') || (chart6 == 'e'))) || ((aff_interface == 1) && (user == 1)) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('J');
      flag = 1;
      Serial.print('J');
    } // Champs Magnetique
    if (((aff_cons == 1) && (consConfig.charAt(9) == '1')) || ((aff_graph == 1) && ((chart1 == 'f') || (chart2 == 'f') || (chart3 == 'f') || (chart4 == 'f') || (chart5 == 'f') || (chart6 == 'f'))))
    {
      Serial1.print('K');
      flag = 1;
      Serial.print('K');
    } // ACCELERATION LINEAIRE
    if (((aff_cons == 1) && (consConfig.charAt(10) == '1')) || ((aff_graph == 1) && ((chart1 == 'g') || (chart2 == 'g') || (chart3 == 'g') || (chart4 == 'g') || (chart5 == 'g') || (chart6 == 'g'))) || ((aff_interface == 1) && (user == 1)) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('L');
      flag = 1;
      Serial.print('L');
    } // Vecteur Gravite
    if (((aff_cons == 1) && (consConfig.charAt(11) == '1')) || ((aff_graph == 1) && ((chart1 == 'l') || (chart2 == 'l') || (chart3 == 'l') || (chart4 == 'l') || (chart5 == 'l') || (chart6 == 'l'))) || ((aff_lora == 1) && (LoraStatus == 1)))
    {
      Serial1.print('M');
      flag = 1;
      Serial.print('M');
    } // LUMINANCE
    if (((aff_cons == 1) && (consConfig.charAt(12) == '1')) || ((aff_lora == 1) && (LoraStatus == 1)) || (aff_modeGnss == 1))
    {
      Serial1.print('N');
      flag = 1;
      Serial.print('N');
    } // GNSS
    if ((aff_cons == 1) && (consConfig.charAt(13) == '1'))
    {
      Serial1.print('O');
      flag = 1;
      Serial.print('O');
    } // NMEA
    Serial1.print('Z');
    flag = 0;
    Serial.println('Z'); // if ((flag == 1)||(aff_interface == 1)) { Serial1.print('Z'); flag = 0;Serial.println('Z');}
  }
  aff_cons = 0;
  aff_graph = 0;
  aff_interface = 0;
  aff_lora = 0;
  aff_modeGnss = 0;
  // if (consConfig == "00000000000000"){affCons_ex=0; }
  if ((chart1 == '0') && (chart2 == '0') && (chart3 == '0') && (chart4 == '0') && (chart5 == '0') && (chart6 == '0'))
  {
    affGraph_ex = 0;
  }
}
//*******************************************************************
void serialRead()
{
  // Serial.println("... new HELTEC reception event ...");
  inChar = Serial1.read();
  Serial.print("1er Char recu : ");
  Serial.println(inChar);

  // AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST AUTOTEST
  if (inChar == 'A')
  { // Caractere code pour demander a la carte calculateur de lancer un AUTOTEST sur la carte capteurs
    Temp_String = Serial1.readStringUntil('@');
    //    Serial.println(Temp_String);

    String varTest1, varTest2, varTest3, varTest4, varTest5, varTest6, varTest7, varTest8, varTest9, varTest10, varTest11, varTest12, varTest13, varTest14;

    varTest1 = WIFImodeRead();
    varTest2 = WIFIpowerRead();
    varTest3 = WiFi.softAPIP().toString();
    varTest4 = pingCamera();
    varTest5 = LoRa.getTxPower();
    varTest6 = LoRa.getSpreadingFactor();
    varTest7 = LoRa.getSignalBandwidth();
    varTest8 = LoRa.getFrequency();
    varTest9 = LoRa.getCodingRate4();
    varTest10 = LoRa.getPreambleLength();
    varTest11 = "";
    varTest12 = "";
    varTest13 = "";
    varTest14 = Temp_String;

    AUTOtEST["var1"] = varTest1;
    AUTOtEST["var2"] = varTest2;
    AUTOtEST["var3"] = varTest3;
    AUTOtEST["var4"] = varTest4;
    AUTOtEST["var5"] = varTest5;
    AUTOtEST["var6"] = varTest6;
    AUTOtEST["var7"] = varTest7;
    AUTOtEST["var8"] = varTest8;
    AUTOtEST["var9"] = varTest9;
    AUTOtEST["var10"] = varTest10;
    AUTOtEST["var11"] = varTest11;
    AUTOtEST["var12"] = varTest12;
    AUTOtEST["var13"] = varTest13;
    AUTOtEST["var14"] = varTest14;

    String test_result = JSON.stringify(AUTOtEST);

    events4.send(test_result.c_str(), "TEST_readings", millis());
    Serial.println(" ... Event TEST_readings envoye ...");
    Temp_String = "";
    autoTesting = 0;
    startTime = millis();

    if (len > 0)
    {

      ReplyBuffer = "A" + varTest1 + "#" + varTest2 + "#" + varTest3 + "#" + varTest4 + "#" + varTest5 + "#" + varTest6 + "#" + varTest7 + "#" + varTest8 + "#" + varTest9 + "#" + varTest10 + "#" + varTest11 + "#" + varTest12 + "#" + varTest13 + "#" + varTest14 + "@";
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
      Udp.printf(ReplyBuffer.c_str());
      Serial.println(ReplyBuffer.c_str());
      Udp.printf("\r\n");
      Udp.endPacket();
      ReplyBuffer = "";
    }
  }

  // EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS EPS
  if (inChar == 'B')
  {
    Temp_String = Serial1.readStringUntil('@');
    // Serial.println(Temp_String);
    int pos1 = Temp_String.indexOf('#');
    int pos2 = Temp_String.indexOf('#', pos1 + 1);
    int pos3 = Temp_String.indexOf('#', pos2 + 1);
    int pos4 = Temp_String.indexOf('#', pos3 + 1);
    int pos5 = Temp_String.indexOf('#', pos4 + 1);
    int pos6 = Temp_String.indexOf('#', pos5 + 1);

    var1 = Temp_String.substring(0, pos1);
    var2 = Temp_String.substring(pos1 + 1, pos2);
    var3 = Temp_String.substring(pos2 + 1, pos3);
    var4 = Temp_String.substring(pos3 + 1, pos4);
    var5 = Temp_String.substring(pos4 + 1, pos5);
    var6 = Temp_String.substring(pos5 + 1, pos6);
    var7 = Temp_String.substring(pos6 + 1, Temp_String.length());

    valeurs[0] = 'B' + Temp_String + "@"; // trame pour la liaison UDP

    Temp_String = "";
  }

  // TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE TEMPERATURE
  if (inChar == 'C')
  {
    Temp_String = Serial1.readStringUntil('@');
    var8 = Temp_String;

    valeurs[1] = 'C' + Temp_String + "@"; // trame pour la liaison UDP

    Temp_String = "";
  }
  // ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE ALTITUDE
  if (inChar == 'D')
  {
    Temp_String = Serial1.readStringUntil('@');
    var9 = Temp_String;

    valeurs[2] = 'D' + Temp_String + "@"; // trame pour la liaison UDP

    Temp_String = "";
  }
  // PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION PRESSION
  if (inChar == 'E')
  {
    Temp_String = Serial1.readStringUntil('@');
    var10 = Temp_String;

    valeurs[3] = 'E' + Temp_String + "@"; // trame pour la liaison UDP

    Temp_String = "";
  }
  // EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER EULER
  if (inChar == 'F')
  {
    Temp_String = Serial1.readStringUntil('@');
    int pos1 = Temp_String.indexOf('#');
    int pos2 = Temp_String.indexOf('#', pos1 + 1);

    var11 = Temp_String.substring(0, pos1);
    var12 = Temp_String.substring(pos1 + 1, pos2);
    var13 = Temp_String.substring(pos2 + 1, Temp_String.length());

    valeurs[4] = 'F' + Temp_String + "@"; // trame pour la liaison UDP
    Temp_String = "";
  }

  // Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion Quaterion

  if (inChar == 'G')
  {
    Temp_String = Serial1.readStringUntil('@');
    int pos1 = Temp_String.indexOf('#');
    int pos2 = Temp_String.indexOf('#', pos1 + 1);
    int pos3 = Temp_String.indexOf('#', pos2 + 1);

    var14 = Temp_String.substring(0, pos1);
    var15 = Temp_String.substring(pos1 + 1, pos2);
    var16 = Temp_String.substring(pos2 + 1, pos3);
    var17 = Temp_String.substring(pos3 + 1, Temp_String.length());

    valeurs[5] = 'G' + Temp_String + "@"; // trame pour la liaison UDP

    Temp_String = "";
  }
  // Vitesse Angulaire Vitesse Angulaire Vitesse Angulaire Vitesse Angulaire Vitesse Angulaire Vitesse Angulaire Vitesse Angulaire Vitesse Angulaire Vitesse Angulaire Vitesse Angulaire

  if (inChar == 'H')
  {
    Temp_String = Serial1.readStringUntil('@');
    int pos1 = Temp_String.indexOf('#');
    int pos2 = Temp_String.indexOf('#', pos1 + 1);

    var18 = Temp_String.substring(0, pos1);
    var19 = Temp_String.substring(pos1 + 1, pos2);
    var20 = Temp_String.substring(pos2 + 1, Temp_String.length());

    valeurs[6] = 'H' + Temp_String + "@"; // trame pour la liaison UDP

    Temp_String = "";
  }

  // Acceleration Acceleration Acceleration Acceleration Acceleration Acceleration Acceleration Acceleration Acceleration Acceleration Acceleration Acceleration Acceleration Acceleration

  if (inChar == 'I')
  {
    Temp_String = Serial1.readStringUntil('@');
    int pos1 = Temp_String.indexOf('#');
    int pos2 = Temp_String.indexOf('#', pos1 + 1);

    var21 = Temp_String.substring(0, pos1);
    var22 = Temp_String.substring(pos1 + 1, pos2);
    var23 = Temp_String.substring(pos2 + 1, Temp_String.length());

    var21B = (atof((var21).c_str())) / 100;
    var22B = (atof((var22).c_str())) / 100;
    var23B = (atof((var23).c_str())) / 100;

    var21 = String(var21B);
    var22 = String(var22B);
    var23 = String(var23B);

    // valeurs[7]= 'I'+Temp_String+ "@";
    valeurs[7] = 'L' + var21 + var22 + var23 + "@"; // trame pour la liaison UDP

    Temp_String = "";
  }

  // Champs Magnetique Champs Magnetique  Champs Magnetique  Champs Magnetique  Champs Magnetique  Champs Magnetique  Champs Magnetique  Champs Magnetique  Champs Magnetique  Champs Magnetique

  if (inChar == 'J')
  {
    Temp_String = Serial1.readStringUntil('@');
    int pos1 = Temp_String.indexOf('#');
    int pos2 = Temp_String.indexOf('#', pos1 + 1);

    var24 = Temp_String.substring(0, pos1);
    var25 = Temp_String.substring(pos1 + 1, pos2);
    var26 = Temp_String.substring(pos2 + 1, Temp_String.length());

    var24B = (atof((var24).c_str())) / 10;
    var25B = (atof((var25).c_str())) / 10;
    var26B = (atof((var26).c_str())) / 10;

    var24 = String(var24B);
    var25 = String(var25B);
    var26 = String(var26B);

    // valeurs[8]= 'J'+Temp_String+ "@"; // trame pour la liaison UDP
    valeurs[8] = 'L' + var24 + var25 + var26 + "@"; // trame pour la liaison UDP
    Temp_String = "";
  }

  // Acceleration Lineaire Acceleration Lineaire Acceleration Lineaire Acceleration Lineaire Acceleration Lineaire Acceleration Lineaire Acceleration Lineaire Acceleration Lineaire

  if (inChar == 'K')
  {
    Temp_String = Serial1.readStringUntil('@');
    int pos1 = Temp_String.indexOf('#');
    int pos2 = Temp_String.indexOf('#', pos1 + 1);

    var27 = Temp_String.substring(0, pos1);
    var28 = Temp_String.substring(pos1 + 1, pos2);
    var29 = Temp_String.substring(pos2 + 1, Temp_String.length());

    var27B = (atof((var27).c_str())) / 100;
    var28B = (atof((var28).c_str())) / 100;
    var29B = (atof((var29).c_str())) / 100;

    var27 = String(var27B);
    var28 = String(var28B);
    var29 = String(var29B);

    // valeurs[9]= 'K'+Temp_String+ "@";
    valeurs[9] = 'L' + var27 + var28 + var29 + "@"; // trame pour la liaison UDP
    Temp_String = "";
  }

  // Vecteur Gravite Vecteur Gravite Vecteur Gravite Vecteur Gravite Vecteur Gravite Vecteur Gravite Vecteur Gravite Vecteur Gravite Vecteur Gravite Vecteur Gravite Vecteur Gravite

  if (inChar == 'L')
  {
    Temp_String = Serial1.readStringUntil('@');
    int pos1 = Temp_String.indexOf('#');
    int pos2 = Temp_String.indexOf('#', pos1 + 1);

    var30 = Temp_String.substring(0, pos1);
    var31 = Temp_String.substring(pos1 + 1, pos2);
    var32 = Temp_String.substring(pos2 + 1, Temp_String.length());

    var30B = (atof((var30).c_str())) / 100;
    var31B = (atof((var31).c_str())) / 100;
    var32B = (atof((var32).c_str())) / 100;

    var30 = String(var30B);
    var31 = String(var31B);
    var32 = String(var32B);

    // valeurs[10]= 'L'+Temp_String+ "@";
    valeurs[10] = 'L' + var30 + var31 + var32 + "@"; // trame pour la liaison UDP
    Temp_String = "";
  }

  // Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance Luminance

  if (inChar == 'M')
  {
    Temp_String = Serial1.readStringUntil('@');
    int pos1 = Temp_String.indexOf('#');
    int pos2 = Temp_String.indexOf('#', pos1 + 1);
    int pos3 = Temp_String.indexOf('#', pos2 + 1);
    int pos4 = Temp_String.indexOf('#', pos3 + 1);

    var33 = Temp_String.substring(0, pos1);
    var34 = Temp_String.substring(pos1 + 1, pos2);
    var35 = Temp_String.substring(pos2 + 1, pos3);
    var36 = Temp_String.substring(pos3 + 1, pos4);
    var37 = Temp_String.substring(pos4 + 1, Temp_String.length());

    valeurs[11] = 'M' + Temp_String + "@";
    Temp_String = "";
  }

  // GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS GNSS

  if (inChar == 'N')
  {
    Temp_String = Serial1.readStringUntil('@');
    int pos1 = Temp_String.indexOf('#');
    int pos2 = Temp_String.indexOf('#', pos1 + 1);
    int pos3 = Temp_String.indexOf('#', pos2 + 1);

    var38 = Temp_String.substring(0, pos1);
    var39 = Temp_String.substring(pos1 + 1, pos2);
    var40 = Temp_String.substring(pos2 + 1, pos3);
    var41 = Temp_String.substring(pos3 + 1, Temp_String.length());

    valeurs[12] = 'N' + Temp_String + "@"; // trame pour la liaison UDP

    Temp_String = "";
  }

  if (inChar == 'P')
  { // dans le cas ou carte envoie No-data
    Temp_String = Serial1.readStringUntil('@');
    var38 = Temp_String;
    var39 = Temp_String;
    var40 = Temp_String;
    var41 = Temp_String;

    valeurs[12] = 'N' + Temp_String + "@"; // trame pour la liaison UDP

    Temp_String = "";
  }
  // NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA NMEA

  if (inChar == 'O')
  {
    Temp_String = Serial1.readStringUntil('@');
    int L = Temp_String.length();
    Serial.println(L);
    int pos1 = int(L / 9); // Serial.println(pos1);
    int pos2 = 2 * pos1;   // Serial.println(pos2);
    int pos3 = 3 * pos1;   // Serial.println(pos3);
    int pos4 = 4 * pos1;   // Serial.println(pos4);
    int pos5 = 5 * pos1;   // Serial.println(pos5);
    int pos6 = 6 * pos1;   // Serial.println(pos6);
    int pos7 = 7 * pos1;   // Serial.println(pos7);
    int pos8 = 8 * pos1;   // Serial.println(pos8);

    var42 = Temp_String.substring(0, pos1);
    var43 = Temp_String.substring(pos1, pos2);
    var44 = Temp_String.substring(pos2, pos3);
    var45 = Temp_String.substring(pos3, pos4);
    var46 = Temp_String.substring(pos4, pos5);
    var47 = Temp_String.substring(pos5, pos6);
    var48 = Temp_String.substring(pos6, pos7);
    var49 = Temp_String.substring(pos7, pos8);
    var50 = Temp_String.substring(pos8, L);

    valeurs[13] = 'O' + Temp_String + "@"; // trame pour la liaison UDP

    Temp_String = "";
  }
  if (inChar == 'Q')
  { // dans le cas ou carte envoie No-data
    Temp_String = Serial1.readStringUntil('@');
    var42 = Temp_String;
    var43 = "";
    var44 = "";
    var45 = "";
    var46 = "";
    var47 = "";
    var48 = "";
    var49 = "";
    var50 = "";

    valeurs[13] = 'O' + Temp_String + "@"; // trame pour la liaison UDP
    Temp_String = "";
  }

  // FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN FIN

  if (inChar == 'Z')
  { // code pour indiquer la fin des parametres choisi, et envoyer les resultats vers la console avec l'event

    if (affCons_ex == 1)
    {
      sendEventCons();
      if (udp_Ex == 1)
      {
        Serial.print("Envoi des trames UDP ..");

        for (int i = 0; i < 14; i++)
        {
          // Si le champs est demande dans la requete
          if (consConfig.charAt(i) == '1')
          {
            // Alors envoyer le paquet correspondant
            Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
            Udp.printf(valeurs[i].c_str());
            Udp.printf("\r\n");
            Udp.endPacket();
            // Serial.println(valeurs[i].c_str()) ;
          }
        }
      }
      affCons_ex = 0;
    }
    if (affGraph_ex == 1)
    {
      sendEventGraph();
      affGraph_ex = 0;
    }
    if (affInt_ex == 1)
    {
      sendEventIntf();
      affInt_ex = 0;
    }
    if (modeGnss_ex == 1)
    {
      file_SPIFFS();
      modeGnss_ex = 0;
    }
    if ((affLora_ex == 1) && (LoraStatus == 1))
    {
      Serial.println("Lora Sending");
      digitalWrite(SS, LOW); //<<<<<<<<<<<< selectionner SPI LORA
      String LoRaMessage = Readings3();
      // Send LoRa packet to receiver
      LoRa.beginPacket();
      LoRa.print(LoRaMessage);
      LoRa.endPacket();

      Serial.print("Envoi de la trame LORA N°: ");
      Serial.println(readingID);
      Serial.print(LoRaMessage);
      delay(200);

      readingID += 1;
      affLora_ex = 0;
      //{"var1":"7","var2":"","var3":"","var4":"36","var5":"","var6":"53","var7":"","var8":"76","var9":"86","var10":"92","var11":"106","var12":"117","var13":"128","var14":"","var15":"","var16":"","var17":"","var18":"171","var19":"184","var20":"195","var21":"204","var22":"217","var23":"223","var24":"238","var25":"246","var26":"251","var27":"","var28":"","var29":"","var30":"295","var31":"301","var32":"316","var33":"","var34":"","var35":"","var36":"","var37":"","var38":"","var39":"","var40":"","var41":""}****************console
    }
  }
}

// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
// Retourner une chaine de caractere representative de l'etat du serveur
String getState()
{
  return "S" + String(CamStatus) + "#" + String(LoraStatus) + "#" + "Capteurs OK" + "#" + String(console_intv) + "#" + String(modeGnss) + "@";
}

void fileTx()
{ // fonction pour l'envoie des resultats du nmode GNSS sur la liaison UDP
  File file2 = SPIFFS.open("/Trajectoire_GNSS.txt", "r");

  if (!file2)
  {
    Serial.println("Failed to open file for reading");
    return;
  }

  Serial.println("File Content:");

  while (file2.available())
  {
    // String fileChar = String(file2.read());
    String fileLine = "W" + file2.readStringUntil('\n') + "@";
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.printf(fileLine.c_str());
    Udp.printf("\r\n");
    Udp.endPacket();
    delay(100);
    Serial.print(fileLine);
  }

  file2.close();

  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  String Reply = "W#@";
  Udp.printf(Reply.c_str());
  Udp.printf("\r\n");
  Udp.endPacket();
}

int isNumeric(String str)
{ // fonction pour tester si un string contien un numéro en lui

  int result = 1;
  for (int i = 0; i < str.length(); i++)
  {
    if (!isDigit(str.charAt(i)))
    {
      if (str.charAt(i) != '-')
      {
        result = 0;
        break;
      }
    }
  }
  return result;
}

void tstMag1()
{ // fonction pour exécuter le test mangnétocoupleurs 1
  int sensX, sensY;
  int Sx, Ix, Sy, Iy;
  int Imax = 150;
  int p = 90; // 5 5  bien, 15 15 bien; 30 15 bien plus lente; 60 15 bien plus lente; 60 10 bien plus lente; 10 10 bien; 100 15 tres bien lente; (60 83 top)
  int t = 34; // 180 123 ; 120 83
  while (testmg)
  {
    // phase 1
    sensX = 0;
    sensY = 1;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = j;
      Sy = 255 - j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 2
    sensX = 0;
    sensY = 0;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = 255 - j;
      Sy = j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 3
    sensX = 1;
    sensY = 0;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = j;
      Sy = 255 - j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 4
    sensX = 1;
    sensY = 1;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = 255 - j;
      Sy = j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }
  }
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);
  ledcWrite(ChannelX, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
  delay(100);
  ledcWrite(ChannelY, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
  delay(100);

  // Serial.println (testfin);
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);
  if (len > 0)
  {

    ReplyBuffer = "Test fini.";
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.printf(ReplyBuffer.c_str());
    Serial.println(ReplyBuffer.c_str());
    Udp.printf("\r\n");
    Udp.endPacket();
    ReplyBuffer = "";
  }
}

void tstMag2()
{ // fonction pour exécuter le test mangnétocoupleurs 2
  int sensX, sensY;
  int Sx, Ix, Sy, Iy;
  int Imax = 150;
  int p = 450; // 5 5  bien, 15 15 bien; 30 15 bien plus lente; 60 15 bien plus lente; 60 10 bien plus lente; 10 10 bien; 100 15 tres bien lente; (60 83 top)
  int t = 34;  // 180 123 ; 120 83
  while (testmg)
  {
    // phase 1
    sensX = 0;
    sensY = 1;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = j;
      Sy = 255 - j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 2
    sensX = 0;
    sensY = 0;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = 255 - j;
      Sy = j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 3
    sensX = 1;
    sensY = 0;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = j;
      Sy = 255 - j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 4
    sensX = 1;
    sensY = 1;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax + t; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = 255 - j;
      Sy = j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }
  }
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);
  ledcWrite(ChannelX, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
  delay(100);
  ledcWrite(ChannelY, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
  delay(100);

  // Serial.println (testfin);
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);
  if (len > 0)
  {

    ReplyBuffer = "Test fini.";
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.printf(ReplyBuffer.c_str());
    Serial.println(ReplyBuffer.c_str());
    Udp.printf("\r\n");
    Udp.endPacket();
    ReplyBuffer = "";
  }
}

void tstMag3()
{ // fonction pour exécuter le test mangnétocoupleurs 3
  int sensX, sensY;
  int Sx, Ix, Sy, Iy;
  int Imax = 150;
  int p = 90; // 5 5  bien, 15 15 bien; 30 15 bien plus lente; 60 15 bien plus lente; 60 10 bien plus lente; 10 10 bien; 100 15 tres bien lente; (60 83 top)
  int t = 34; // 180 123 ; 120 83
  while (testmg)
  {

    // phase 1
    sensX = 1;
    sensY = 1;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = j;
      Sy = 255 - j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 2
    sensX = 1;
    sensY = 0;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = 255 - j;
      Sy = j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 3
    sensX = 0;
    sensY = 0;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = j;
      Sy = 255 - j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 4
    sensX = 0;
    sensY = 1;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = 255 - j;
      Sy = j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }
  }
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);
  ledcWrite(ChannelX, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
  delay(100);
  ledcWrite(ChannelY, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
  delay(100);

  // Serial.println (testfin);
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);
  if (len > 0)
  {

    ReplyBuffer = "Test fini.";
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.printf(ReplyBuffer.c_str());
    Serial.println(ReplyBuffer.c_str());
    Udp.printf("\r\n");
    Udp.endPacket();
    ReplyBuffer = "";
  }
}

void tstMag4()
{ // fonction pour exécuter le test mangnétocoupleurs 4
  int sensX, sensY;
  int Sx, Ix, Sy, Iy;
  int Imax = 150;
  int p = 450; // 5 5  bien, 15 15 bien; 30 15 bien plus lente; 60 15 bien plus lente; 60 10 bien plus lente; 10 10 bien; 100 15 tres bien lente; (60 83 top)
  int t = 34;  // 180 123 ; 120 83
  while (testmg)
  {

    // phase 1
    sensX = 1;
    sensY = 1;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = j;
      Sy = 255 - j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 2
    sensX = 1;
    sensY = 0;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = 255 - j;
      Sy = j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 3
    sensX = 0;
    sensY = 0;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = j;
      Sy = 255 - j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }

    // phase 4
    sensX = 0;
    sensY = 1;
    digitalWrite(sensPin, sensX);  // changement du sens du courant pin 25
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33

    for (int j = 255; j >= Imax; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = 255 - j;
      Sy = j;
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
      delay(p);
    }
  }
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);
  ledcWrite(ChannelX, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
  delay(100);
  ledcWrite(ChannelY, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
  delay(100);

  // Serial.println (testfin);
  delay(100);
  events5.send(testfin.c_str(), "fct_fin", millis());
  delay(100);

  if (len > 0)
  {

    ReplyBuffer = "Test fini.";
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.printf(ReplyBuffer.c_str());
    Serial.println(ReplyBuffer.c_str());
    Udp.printf("\r\n");
    Udp.endPacket();
    ReplyBuffer = "";
  }
}
// FONCTION DEMAGNETISATION DEMAGNETISATION DEMAGNETISATION DEMAGNETISATION DEMAGNETISATION DEMAGNETISATION DEMAGNETISATION DEMAGNETISATION DEMAGNETISATION DEMAGNETISATION DEMAGNETISATION
void deMag()
{
  /*
  int dfreq = 10 ; // frequence de la sinusoide de demagnetisation en Hz
  float dtemps = 1/(dfreq*360)*1000*1000; // interval d'echantillonnage de la sinusoide en microseconde = 277 us
  int dDuree = 5000;  // duree de la demagnetisation : 5 s ici
  int sensX, sensY;
  float sinX, sinY;
  unsigned long sinIntv;
  unsigned long dbegin;

  dbegin = millis();   // debut de la demagnetisation du magneto-coupleur X
  while (millis() - dbegin < dDuree) {
   sensX = 0;
  for (int j=0; j<=180; j++){
  sinX = sin(j*3.14159265/180)*(-(millis()-dbegin)/(dDuree)+1);
  int Sx = map((sinX*100), 100, 0, 0, 255);

digitalWrite(sensPin, sensX); // changement du sens du courant pin 25
ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
  sinIntv = micros();
    while (micros() - sinIntv < dtemps) {}
  }
   sensX = 1;
  for (int j=0; j<=180; j++){
  sinX = sin(j*3.14159265/180)*(-(millis()-dbegin)/(dDuree)+1);
  int Sx = map((sinX*100), 100, 0, 0, 255);

digitalWrite(sensPin, sensX); // changement du sens du courant pin 25
ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
  sinIntv = micros();
    while (micros() - sinIntv < dtemps) {}
  }

  }


    dbegin = millis(); // debut de la demagnetisation du magneto-coupleur Y
  while (millis() - dbegin < dDuree) {
   sensY = 0;
  for (int j=0; j<=180; j++){
  sinY = sin(j*3.14159265/180)*(-(millis()-dbegin)/(dDuree)+1);
  int Sy = map((sinY*100), 100, 0, 0, 255);

digitalWrite(sensPinY, sensY); // changement du sens du courant pin 25
ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
  sinIntv = micros();
    while (micros() - sinIntv < dtemps) {}
  }
   sensY = 1;
  for (int j=0; j<=180; j++){
  sinY = sin(j*3.14159265/180)*(-(millis()-dbegin)/(dDuree)+1);
  int Sy = map((sinY*100), 100, 0, 0, 255);

digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33
ledcWrite(ChannelY, Sy); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
  sinIntv = micros();
    while (micros() - sinIntv < dtemps) {}
  }

  }


  demag = 0;
  String dmagFin ="A";
  Serial.println (dmagFin);
  events5.send(dmagFin.c_str(),"fct_fin",millis());

  ledcWrite(ChannelX, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
  ledcWrite(ChannelY, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
*/

  // démagnétisation, solution 2, signaux linéaires

  int sensX, sensY;
  int Sx, Ix, Sy, Iy;
  int Imin = 250;
  int p = 20;
  int t = 40;
  int N = 20;
  float F = 1;
  //// Magnéto X ********
  while (N)
  {

    // phase 1
    sensX = 0;
    digitalWrite(sensPin, sensX); // changement du sens du courant pin 25
    for (int j = 255; j >= 135; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = int(j * F);
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      delay(p);
    }

    // phase 2
    sensX = 0;
    digitalWrite(sensPin, sensX); // changement du sens du courant pin 25
    for (int j = 175; j <= 255; j = j + t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = int(j * F);
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      delay(p);
    }

    // phase 3
    sensX = 1;
    digitalWrite(sensPin, sensX); // changement du sens du courant pin 25
    for (int j = 215; j >= 135; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = int(j * F);
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      delay(p);
    }

    // phase 4
    sensX = 1;
    digitalWrite(sensPin, sensX); // changement du sens du courant pin 25
    for (int j = 175; j <= 215; j = j + t)
    { // 255 = 0V   ; 0 = 5V;
      Sx = int(j * F);
      ledcWrite(ChannelX, Sx); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
      delay(p);
    }
    N = N - 1;
    F = F - 0.1;
  }
  //// Magnéto Y ********
  N = 20;
  F = 1;
  while (N)
  {
    // phase 1
    sensY = 0;
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 25
    for (int j = 255; j >= 135; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sy = int(j * F);
      ledcWrite(ChannelY, Sy);
      delay(p);
    }

    // phase 2
    sensY = 0;
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 25
    for (int j = 175; j <= 255; j = j + t)
    { // 255 = 0V   ; 0 = 5V;
      Sy = int(j * F);
      ledcWrite(ChannelY, Sy);
      delay(p);
    }

    // phase 3
    sensY = 1;
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 25
    for (int j = 215; j >= 135; j = j - t)
    { // 255 = 0V   ; 0 = 5V;
      Sy = int(j * F);
      ledcWrite(ChannelY, Sy);
      delay(p);
    }

    // phase 4
    sensY = 1;
    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 25
    for (int j = 175; j <= 215; j = j + t)
    { // 255 = 0V   ; 0 = 5V;
      Sy = int(j * F);
      ledcWrite(ChannelY, Sy);
      delay(p);
    }
    N = N - 1;
    F = F - 0.1;
  }
  delay(100);
  demag = 0;
  delay(100);
  dmagFin = "A";
  //  Serial.println (dmagFin);
  delay(100);
  events5.send(dmagFin.c_str(), "fct_fin", millis());
  delay(200);
  ledcWrite(ChannelX, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 23
  delay(100);
  ledcWrite(ChannelY, 255); // changement de l'intensite du courant via le rapport cyclique pwm pin 32
  delay(100);

  events5.send(dmagFin.c_str(), "fct_fin", millis());
  delay(100);

  if (len > 0)
  {

    ReplyBuffer = " .. Demagnetisation Finie";
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.printf(ReplyBuffer.c_str());
    Serial.println(ReplyBuffer.c_str());
    Udp.printf("\r\n");
    Udp.endPacket();
    ReplyBuffer = "";
  }
}

<<<<<<< HEAD
//SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP
void setup() {
delay(100);
ledcSetup(ChannelX, freq, resolution);
delay(100);
ledcAttachPin(pwmPin, ChannelX);
delay(100);
ledcWrite(ChannelX, 255);
delay(100);

ledcSetup(ChannelY, freqY, resolutionY);
delay(100);
ledcAttachPin(pwmPinY, ChannelY);
delay(100);
ledcWrite(ChannelY, 255);
delay(100);

Serial.begin(115200);
Serial1.begin(115200);
Serial1.setRxBufferSize(2048);
Temp_String.reserve(2048);

tstMag1();
delay(100);
tstMag2();
delay(100);
tstMag3();
delay(100);
tstMag1();
delay(100);

pinMode(LORA_LED , OUTPUT);  // LED LIAISON LORA
pinMode(COMM_LED , OUTPUT);  // LED CONFIGURATION WIFI ET SPIFFS
pinMode(CAM_STATUT , OUTPUT);  // LED CONFIGURATION WIFI ET SPIFFS
digitalWrite(LORA_LED, LOW); // LED CONFIGURATION LORA
digitalWrite(COMM_LED, LOW); // LED CONFIGURATION WIFI ET SPIFFS
digitalWrite(CAM_STATUT, LOW); // LED CONFIGURATION WIFI ET SPIFFS



initWiFi();
delay(200);
initSPIFFS();
delay(200);
if ((wifiOk==1)&&(spiffsOk==1)){digitalWrite(COMM_LED, HIGH);} // // LED CONFIGURATION WIFI ET SPIFFS OK
startLoRA();
delay(200);
if (loraOk ==1) {digitalWrite(LORA_LED, LoraStatus); }// LED LIAISON LORA

pinMode(sensPin , OUTPUT); // Roue a Inertie
pinMode(sensPinY , OUTPUT);

//pinMode(pwmPin , OUTPUT);



// SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER
server.begin();
server.addHandler(&events);
server.addHandler(&events2);
server.addHandler(&events3);
server.addHandler(&events4);
server.addHandler(&events5);


//esp_task_wdt_init(WDT_TIMEOUT, true); //enable panic so ESP32 restarts
//esp_task_wdt_add(NULL); //add current thread to WDT watch

// Route for root / web page
/*##################
server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
request->send(SPIFFS, "/index.html", String(), false);
  });
=======
// SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP
void setup()
{
  delay(100);
  ledcSetup(ChannelX, freq, resolution);
  delay(100);
  ledcAttachPin(pwmPin, ChannelX);
  delay(100);
  ledcWrite(ChannelX, 255);
  delay(100);
>>>>>>> 89c6c53a3f3aa35f520df8c308bcf2ccf2e90ad9

  ledcSetup(ChannelY, freqY, resolutionY);
  delay(100);
  ledcAttachPin(pwmPinY, ChannelY);
  delay(100);
  ledcWrite(ChannelY, 255);
  delay(100);

<<<<<<< HEAD
server.on("/telecommandes.html", HTTP_GET, [](AsyncWebRequest *request){
request->send(SPIFFS, "/telecommandes.html", String(), false, processor);
  });
server.serveStatic("/", SPIFFS, "/");

// evenement pour agir lors des changement des bouttons de la partie controle**************************************************************************************
################*/
=======
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial1.setRxBufferSize(2048);
  Temp_String.reserve(2048);

  tstMag1();
  delay(100);
  tstMag2();
  delay(100);
  tstMag3();
  delay(100);
  tstMag1();
  delay(100);

  pinMode(LORA_LED, OUTPUT);     // LED LIAISON LORA
  pinMode(COMM_LED, OUTPUT);     // LED CONFIGURATION WIFI ET SPIFFS
  pinMode(CAM_STATUT, OUTPUT);   // LED CONFIGURATION WIFI ET SPIFFS
  digitalWrite(LORA_LED, LOW);   // LED CONFIGURATION LORA
  digitalWrite(COMM_LED, LOW);   // LED CONFIGURATION WIFI ET SPIFFS
  digitalWrite(CAM_STATUT, LOW); // LED CONFIGURATION WIFI ET SPIFFS
>>>>>>> 89c6c53a3f3aa35f520df8c308bcf2ccf2e90ad9

  initWiFi();
  delay(200);
  initSPIFFS();
  delay(200);
  if ((wifiOk == 1) && (spiffsOk == 1))
  {
    digitalWrite(COMM_LED, HIGH);
  } // // LED CONFIGURATION WIFI ET SPIFFS OK
  startLoRA();
  delay(200);
  if (loraOk == 1)
  {
    digitalWrite(LORA_LED, LoraStatus);
  } // LED LIAISON LORA

  pinMode(sensPin, OUTPUT); // Roue a Inertie
  pinMode(sensPinY, OUTPUT);

  // pinMode(pwmPin , OUTPUT);

  // SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER SERVER
  server.begin();
  server.addHandler(&events);
  server.addHandler(&events2);
  server.addHandler(&events3);
  server.addHandler(&events4);
  server.addHandler(&events5);

  // esp_task_wdt_init(WDT_TIMEOUT, true); //enable panic so ESP32 restarts
  // esp_task_wdt_add(NULL); //add current thread to WDT watch

  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request)
            { request->send(SPIFFS, "/index.html", String(), false); });

  server.on("/controle.html", HTTP_GET, [](AsyncWebServerRequest *request)
            { request->send(SPIFFS, "/controle.html", String(), false, processor); });

  server.on("/telecommandes.html", HTTP_GET, [](AsyncWebServerRequest *request)
            { request->send(SPIFFS, "/telecommandes.html", String(), false, processor); });
  server.serveStatic("/", SPIFFS, "/");

  // evenement pour agir lors des changement des bouttons de la partie controle**************************************************************************************

  server.on("/LoraOFF", HTTP_GET, [](AsyncWebServerRequest *request) { // button active/desactivation liaison LORA****************************************************
    // Serial.println(LoraStatus);
    LoraStatus = 0;
    if (loraOk == 1)
    {
      digitalWrite(LORA_LED, LoraStatus); // LED LIAISON LORA
      Serial.println("... Liaison LORA Desactivee ...");
      request->send_P(200, "text/plain", "Liaison Lora Desactivée ..");
    }
    else
    {
      request->send_P(200, "text/plain", "Défaut sur la liaison LORA !");
    }
  });

  server.on("/LoraON", HTTP_GET, [](AsyncWebServerRequest *request)
            {
      LoraStatus = 1;
      if (loraOk ==1) {digitalWrite(LORA_LED, LoraStatus);
      Serial.println("... Liaison LORA Activee ...");// LED LIAISON LORA
  request->send_P(200, "text/plain", "Liaison Lora Activée ..");}
  else {request->send_P(200, "text/plain", "Défaut sur la liaison LORA !");} });

  server.on("/CamOFF", HTTP_GET, [](AsyncWebServerRequest *request) { // button active/desactivation CAM*************************************************************
    CamStatus = 0;
    digitalWrite(CAM_STATUT, CamStatus);
    Serial.println("... Camera desactivee ...");
    request->send_P(200, "text/plain", "Camera Desactivée ..");
  });
  server.on("/CamON", HTTP_GET, [](AsyncWebServerRequest *request)
            {
      CamStatus = 1;
      digitalWrite(CAM_STATUT, CamStatus);
      Serial.println("... Camera Activee ...");
  request->send_P(200, "text/plain", "Camera Activée .."); });

  /*
  server.on("/Cap9OFF", HTTP_GET, [](AsyncWebServerRequest *request){ // button active/desactivation Capteur 9 Axes***************************************************
     Cap9Axes = 0;
     Serial.println(" Capteur 9 Axes desactive ...");
  request->send(200, "text/plain", "OK");
  });
  server.on("/Cap9ON", HTTP_GET, [](AsyncWebServerRequest *request){
        Cap9Axes = 1;
        Serial.println(" Captueur 9 Axes active ...");
    request->send(200, "text/plain", "OK");
    });
  */

  /*
  server.on("/Rgs", HTTP_GET, [](AsyncWebServerRequest *request){
  file_SPIFFS() ;
  request->send(200, "/index.html", "OK");
    });
  */

  /*
    // Handle Web Server Events
   events.onConnect([](AsyncEventSourceClient *client){
      if(client->lastId()){
        Serial.printf("Client reconnected! Last message ID that it got is: %u\n", client->lastId());
      }
      // send event with message "hello!", id current millis
      // and set reconnect delay to 1 second
      client->send("hello!", NULL, millis(), 10000);
    });
  */

  server.on("/ouvPage", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour envoyer les parametres en-cours pour initialiser la page index et les autres (dans une variable json)
    user = 1;
    // Serial.println("user= "); Serial.println(user);
    user_start = millis();
    // Serial.println("millis()= "); Serial.println(millis()); //Serial.println("user_start= "); Serial.println(user_start);
    // CamStatus = 0;
    // LoraStatus = 0;
    // console_intv = 5000;
    // graph_intv = 5000;
    // angRotCoup = 0;
    // consConfig = "00000000000000";
    chart1 = '0';
    chart2 = '0';
    chart3 = '0';
    chart4 = '0';
    chart5 = '0';
    chart6 = '0';
    // request->send(200, "text/plain", "OK");

    Index_init["cam"] = CamStatus;
    Index_init["lora"] = LoraStatus;
    Index_init["console_intv"] = console_intv;
    Index_init["graph_intv"] = graph_intv;
    Index_init["consf"] = consConfig;
    String temp_init = JSON.stringify(Index_init);
    request->send_P(200, "text/plain", temp_init.c_str());
    Serial1.print('B');
    Serial.print('B');
    Serial1.print('I');
    Serial.print('I');
    Serial1.print('H');
    Serial.print('H');
    Serial1.print('J');
    Serial.print('J');
    Serial1.print('L');
    Serial.print('L');
    Serial1.print('F');
    Serial.print('F');
    Serial1.print('C');
    Serial.print('C');
    Serial1.print('D');
    Serial.print('D');
    Serial1.print('E');
    Serial.print('E');
    Serial1.print('Z');
    Serial.println('Z');
    affInt_ex = 1;
    affCons_ex = 0;
    affGraph_ex = 0;
  });
  /*
  server.on("/fermPage", HTTP_GET, [](AsyncWebServerRequest *request){
  chart1 = '0'; chart2 = '0';chart3 = '0';chart4 = '0';chart5 = '0';chart6 = '0';
  CamStatus = 0;
  LoraStatus = 0;
  INTV = 5000;
  angRotCoup = 0;
  consConfig = "00000000000000";
  Serial.print("Pages Interface Fermees " );
  request->send(200, "text/plain", "OK");
   });
   */
  server.on("/t_console", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour changer la periode de la console sur la variable INTV + envoyer un message de confirmation
    // Serial1.flush();
    String inputMessage;
    if (request->hasParam("choix"))
    {
      inputMessage = request->getParam("choix")->value();
      console_intv = atoi((inputMessage).c_str()) * 1000;
    }
    Serial.print("Periode choisie : ");
    Serial.print(console_intv / 1000);
    Serial.println(" secondes");
    inputMessage = "Periode choisie : " + String(console_intv / 1000) + " secondes !";
    request->send_P(200, "text/plain", inputMessage.c_str());
  });

  server.on("/t_graph", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour changer la periode de la console sur la variable INTV + envoyer un message de confirmation
    // Serial1.flush();
    String inputMessage;
    if (request->hasParam("choix"))
    {
      inputMessage = request->getParam("choix")->value();
      graph_intv = atoi((inputMessage).c_str()) * 1000;
    }
    Serial.print("Periode graphique choisie : ");
    Serial.print(graph_intv / 1000);
    Serial.println(" secondes");
    inputMessage = "Periode choisie : " + String(graph_intv / 1000) + " secondes !";
    request->send_P(200, "text/plain", inputMessage.c_str());
  });

  server.on("/ang_couple", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour lire l'angle de la commande rotation entre par l'utilisateur, et le mettre dans la variable angRotCoup + envoyer un message de confirmation
    String inputMessage;
    if (request->hasParam("choix"))
    {
      inputMessage = request->getParam("choix")->value();
      angRotCoup = atoi((inputMessage).c_str());
    }

    float Bx = atoi((var24).c_str());
    float By = atoi((var25).c_str());
    float angB = round(atan2(By, Bx) * 180 / 3.14159265);
    float angTot = angB - angRotCoup;
    if (angTot > 360)
    {
      angTot = angTot - 360;
    }
    if (angTot < -360)
    {
      angTot = angTot + 360;
    }
    float ix = cos(angTot * 3.14159265 / 180);
    float iy = sin(angTot * 3.14159265 / 180);
    int sensX, sensY;
    if (ix > 0)
    {
      sensX = 0;
    }
    else
      sensX = 1;
    if (iy > 0)
    {
      sensY = 0;
    }
    else
      sensY = 1;

    int Ix = map(abs(ix * 100), 100, 0, 150, 255);
    int Iy = map(abs(iy * 100), 100, 0, 150, 255);

    digitalWrite(sensPin, sensX); // changement du sens du courant pin 25
    ledcWrite(ChannelX, Ix);      // changement de l'intensite du courant via le rapport cyclique pwm pin 23

    digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33
    ledcWrite(ChannelY, Iy);       // changement de l'intensite du courant via le rapport cyclique pwm pin 32

    /* pour affichage si besoin
    Serial.println(Bx);
    Serial.println(By);
    Serial.println(angB);
    Serial.println(angTot);
    Serial.println(ix);
    Serial.println(iy);
    Serial.println(Ix);
    Serial.println(Iy);
    */

    Serial.print("L'angle de rotation choisi (°): ");
    Serial.println(angRotCoup);
    inputMessage = "Commande lancée pour : " + String(angRotCoup) + "°.";
    request->send_P(200, "text/plain", inputMessage.c_str());
  });

  server.on("/demag", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour lancer la démagnétisation des magnétocpuoleurs
    Serial.println("Demagnetisation lancee ..");
    String inputMessage = "Démagnetisation lancée ..";
    demag = 1;
    request->send_P(200, "text/plain", inputMessage.c_str());
  });

  server.on("/tst1", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour lancer le test magnétocoupleur 1
    Serial.println("Test S1-V1 lance ..");
    String inputMessage = "Test S1-V1 lancé ..";
    testmg = 1;
    request->send_P(200, "text/plain", inputMessage.c_str());
  });

  server.on("/tst2", HTTP_GET, [](AsyncWebServerRequest *request) { // // event pour lancer le test magnétocoupleur 2
    Serial.println("Test S1-V2 lance ..");
    String inputMessage = "Test S1-V2 lancé ..";
    testmg = 2;
    request->send_P(200, "text/plain", inputMessage.c_str());
  });

  server.on("/tst3", HTTP_GET, [](AsyncWebServerRequest *request) { // // event pour lancer le test magnétocoupleur 3
    Serial.println("Test S2-V1 lance ..");
    String inputMessage = "Test S2-V1 lancé ..";
    testmg = 3;
    request->send_P(200, "text/plain", inputMessage.c_str());
  });

  server.on("/tst4", HTTP_GET, [](AsyncWebServerRequest *request) { // // event pour lancer le test magnétocoupleur 4
    Serial.println("Test S2-V2 lance ..");
    String inputMessage = "Test S2-V2 lancé ..";
    testmg = 4;
    request->send_P(200, "text/plain", inputMessage.c_str());
  });

  server.on("/tststp", HTTP_GET, [](AsyncWebServerRequest *request) { // // event pour lancer le test magnétocoupleur 4
    Serial.println("Stop Test lancee ..");
    String inputMessage = "Stop Test lancée ..";
    testmg = 0;
    testfin = "B";
    request->send_P(200, "text/plain", inputMessage.c_str());
  });

  server.on("/roue", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour lire l'angle de la commande rotation entre par l'utilisateur, et le mettre dans la variable angRotCoup + envoyer un message de confirmation
    Serial.print("requete roue recue");                             // Serial.println(vitesse); Serial.println(vitesse);
    String inputMessage;
    if (request->hasParam("choix"))
    {
      inputMessage = request->getParam("choix")->value();
      Roue_Inertie = inputMessage;
    }
    Serial.print("param :");    // Serial.println(vitesse); Serial.println(vitesse);
    Serial.print(inputMessage); // Serial.println(vitesse); Serial.println(vitesse);

    int vitesse = 0;
    int sens = 0;
    char SENS = Roue_Inertie.charAt(0);
    int VITESSE = 255;

    if (SENS == 'S')
    {
      VITESSE = 255;
    }
    else
    {
      if (SENS == 'h')
      {
        sens = 0;
      }
      else
      {
        sens = 1;
      }
      vitesse = atoi((Roue_Inertie.substring(1)).c_str());
      /*
     if (vitesse<=90){ vitesse = vitesse - 20;}

     if (vitesse<0){ vitesse = 0;}
     */
      /*
      int vitesse2;
      if (vitesse>=50){ vitesse2 = map(vitesse, 50, 100, 12, 100);}
        else vitesse2 = map(vitesse, 0, 50, 0, 12);

             VITESSE = map(vitesse2, 100, 0, 0, 255); // VITESSE = map(vitesse, 0, 100, 0, 255);
      */
      VITESSE = map(vitesse, 100, 0, 0, 255);
    }

    ledcWrite(ChannelX, 255);     // ouvrire le transistor P (vitesse nulle)avant le changement du sens pour proteger contre un court circuit eventuelle
    digitalWrite(sensPin, sens);  // changement du sens de rotation pin 25
    ledcWrite(ChannelX, VITESSE); // changement de la vitesse de rotation via rapport cyclique pwm pin 23

    /*/ Variables pour le Magnetocoupleur Y ************************
    const int pwmPinY = 32 ;// 32 corresponds to GPIO32
    const int sensPinY = 33 ; // 33 corresponds to GPIO33
    const int freqY = 1000;
    const int ChannelY = 2;
    const int resolutionY = 8;
    */
    /*
    ledcWrite(ChannelY, 255); // ouvrire le transistor P (vitesse nulle)avant le changement du sens pour proteger contre un court circuit eventuelle
    digitalWrite(sensPinY, sens); // changement du sens de rotation pin 25
    ledcWrite(ChannelY, VITESSE); // changement de la vitesse de rotation via rapport cyclique pwm pin 23
    */
    //  Serial1.print('V'+Roue_Inertie);
    //  Serial.println("Commande lancee pour (R.cyclique): "+String(255-VITESSE)+" ,sense :"+String(SENS));//Serial.println(vitesse); Serial.println(vitesse);
    inputMessage = "Commande lancée pour : " + String(vitesse) + " %, sense : " + String(SENS);
    request->send_P(200, "text/plain", inputMessage.c_str());
  });

  server.on("/cons_config", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour lire la configuraion de la console choisie par l'utilisateur et la mettre dans la variable consConfig
    Serial1.flush();
    String inputMessage;
    // GET input1 value on <ESP_IP>/slider?value=<inputMessage>
    if (request->hasParam("choix"))
    {
      inputMessage = request->getParam("choix")->value();
      consConfig = inputMessage;
    }
    Serial.print("La configuration choisie est : ");
    Serial.print(consConfig);
    // request->send(200, "text/plain", "OK");
    request->send_P(200, "text/plain", "OKOK");
  });

  server.on("/autoTest", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour recevoir la commade AUTOTEST
    // autotest = 1;
    Serial1.flush();
    Serial1.print('A');
    autoTesting = 1;
    Serial.print('A');
    Serial.println("Requete AUTOTEST recue");
    request->send_P(200, "text/plain", "Commande Autotest lancée ..");
  });

  server.on("/user", HTTP_GET, [](AsyncWebServerRequest *request)
            {
user_start = millis();

  Serial.println("user connected ..." );
  request->send(200, "text/plain", "OK"); });

  server.on("/startgnss", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour recevoir la commade de debut du mode trajectoire GNSS
    modeGnss = 1;                                                        // variable utilise pour lancer le mode Releve de trajectoire GNSS
    modeGnss_start = millis();
    Serial1.flush();
    /*
    saveConfig=consConfig;
    consConfig="00000000000000";
    chart1 ='0'; chart2 ='0'; chart3 ='0'; chart4 ='0'; chart5 ='0'; chart6 ='0';
    */
    autoTesting = 1; // ce n'est pas un autotest, mais c'est juste pour mettre en pause l'echang des données pour la console et les graphes pendant que le mode GNSS est exécuté
    String inputMessage;
    if (request->hasParam("choix"))
    {
      inputMessage = request->getParam("choix")->value();

      File file = SPIFFS.open("/Trajectoire_GNSS.txt", "w");
      if (!file)
      {
        Serial.println("Failed to open Trajectoire_GNSS file for save");
        return;
      }
      else
      {
        file.println(inputMessage);
        file.println(" ");
        file.close();
        Serial.println(" Commande recue et fichier .txt cree ... ");
      }
    }
    Serial.println("Requete MODE GNSS recue");
    Serial.println(inputMessage);
    request->send_P(200, "text/plain", "Releve Trajectoire lancée !");
  });

  server.on("/stopgnss", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour recevoir la commade de debut du mode trajectoire GNSS
    modeGnss = 2;                                                       // variable utilise pour lancer le mode Releve de trajectoire GNSS
    // consConfig = saveConfig;
    autoTesting = 0; // arreter la pause et regémarrer la console et la graphes
    Serial.println("Stop MODE GNSS recue");
    request->send_P(200, "text/plain", "Stop Trajectoire lancée !");
  });

  server.on("/savegnss", HTTP_GET, [](AsyncWebServerRequest *request) { // event pour recevoir la commade de debut du mode trajectoire GNSS
    modeGnss = 0;                                                       // variable utilise pour lancer le mode Releve de trajectoire GNSS
    Serial.println("Save MODE GNSS recue");
    request->send_P(200, "text/plain", "Save Trajectoire lancée !");
  });

  // eventes des chartes page graphes pour lire les choix de l'utilisateur sur chacune ***************************************************************************
  server.on("/configGraph1", HTTP_GET, [](AsyncWebServerRequest *request)
            {
  String inputMessage;
  if (request->hasParam("choix")) {
    inputMessage = request->getParam("choix")->value();
    chart1 = inputMessage.charAt(0);
  }
  Serial.print("chart1 : " );Serial.println(chart1);
  request->send(200, "text/plain", "OK"); });
  server.on("/configGraph2", HTTP_GET, [](AsyncWebServerRequest *request)
            {
  String inputMessage;
  if (request->hasParam("choix")) {
    inputMessage = request->getParam("choix")->value();
    chart2 = inputMessage.charAt(0);
  }
  Serial.print("chart2 : " );Serial.println(chart2);
  request->send(200, "text/plain", "OK"); });
  server.on("/configGraph3", HTTP_GET, [](AsyncWebServerRequest *request)
            {
  String inputMessage;
  if (request->hasParam("choix")) {
    inputMessage = request->getParam("choix")->value();
    chart3 = inputMessage.charAt(0);
  }
  Serial.print("chart3 : " );Serial.println(chart3);
  request->send(200, "text/plain", "OK"); });
  server.on("/configGraph4", HTTP_GET, [](AsyncWebServerRequest *request)
            {
  String inputMessage;
  if (request->hasParam("choix")) {
    inputMessage = request->getParam("choix")->value();
    chart4 = inputMessage.charAt(0);
  }
  Serial.print("chart4 : " );Serial.println(chart4);
  request->send(200, "text/plain", "OK"); });
  server.on("/configGraph5", HTTP_GET, [](AsyncWebServerRequest *request)
            {
  String inputMessage;
  if (request->hasParam("choix")) {
    inputMessage = request->getParam("choix")->value();
    chart5 = inputMessage.charAt(0);
  }
  Serial.print("chart5 : " );Serial.println(chart5);
  request->send(200, "text/plain", "OK"); });
  server.on("/configGraph6", HTTP_GET, [](AsyncWebServerRequest *request)
            {
  String inputMessage;
  if (request->hasParam("choix")) {
    inputMessage = request->getParam("choix")->value();
    chart6 = inputMessage.charAt(0);
  }
  Serial.print("chart6 : " );Serial.println(chart6);
  request->send(200, "text/plain", "OK"); });
  //********************************************************************************************************

  startTime = millis(); // initialisation de la variable qui sert a mesurer la periode d'aquisition et d'affichage sur la console
  console_start = millis();
  graph_start = millis();
  interface_start = millis();
  lora_start = millis();

  // startTimeIntf = startTime + INTV/2;
  // LoRa.end();
  // LoRa.idle();
  // LoRa.sleep();

  /*
   Serial.print("LoRa Spreading Factor : "); Serial.println(LoRa.getSpreadingFactor());
   Serial.print("LoRa Signal Bandwidth (Hz): "); Serial.println(LoRa.getSignalBandwidth());
    Serial.print("LoRa Signal Frequency (MHz): "); Serial.println(LoRa.getFrequency());  //
    Serial.print("LoRa Signal Power : (dBm) "); Serial.println(LoRa.getTxPower());
  Serial.print("LoRa Coding Rate (4/x): "); Serial.println(LoRa.getCodingRate4());
  Serial.print("LoRa Preamble Length : "); Serial.println(LoRa.getPreambleLength());
  */

  Udp.begin(localPort); // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
}

// LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP LOOP
void loop()
{

  if ((wifiOk == 1) && (spiffsOk == 1))
  {
    digitalWrite(COMM_LED, LOW);
    digitalWrite(COMM_LED, HIGH);
  } // // LED CONFIGURATION WIFI ET SPIFFS OK
  if (loraOk == 1)
  {
    digitalWrite(LORA_LED, LOW);
    digitalWrite(LORA_LED, LoraStatus);
  }
  digitalWrite(CAM_STATUT, CamStatus);

  if (millis() - startTime >= INTV)
  {

    if ((millis() - user_start >= user_intv) && (udp_Ex == 0))
    {
      user = 0;
      consConfig = "00000000000000";
      chart1 = '0';
      chart2 = '0';
      chart3 = '0';
      chart4 = '0';
      chart5 = '0';
      chart6 = '0';
      Serial.println("user deconnected");
      user_start = millis();
    }

    if (millis() - lora_start >= lora_intv)
    {
      aff_lora = 1;
      affLora_ex = 1;
      lora_start = millis();
    }
    if (millis() - console_start >= console_intv)
    {
      aff_cons = 1;
      affCons_ex = 1;
      console_start = millis();
    }
    if (millis() - graph_start >= graph_intv)
    {
      aff_graph = 1;
      affGraph_ex = 1;
      graph_start = millis();
    }
    if (millis() - interface_start >= interface_intv)
    {
      aff_interface = 1;
      affInt_ex = 1;
      interface_start = millis();
    }
    if (millis() - modeGnss_start >= modeGnss_intv)
    {
      if (modeGnss == 1)
      {
        aff_modeGnss = 1;
        modeGnss_ex = 1;
      }
      modeGnss_start = millis();
    }

    if ((aff_interface == 1) || (aff_cons == 1) || (aff_graph == 1) || (aff_lora == 1) || (aff_modeGnss == 1))
    {
      serialSend();
    }
    startTime = millis();
  }

  if (Serial1.available())
  {
    serialRead();
  }

  if (demag == 1)
  {
    deMag();
  }

  if (testmg == 1)
  {
    tstMag1();
  }

  if (testmg == 2)
  {
    tstMag2();
  }

  if (testmg == 3)
  {
    tstMag3();
  }

  if (testmg == 4)
  {
    tstMag4();
  }

  packetSize = Udp.parsePacket(); // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  if (packetSize)
  {
    len = Udp.read(packetBuffer, 32);
    if (len > 0)
      packetBuffer[len] = 0;
    Serial.println("Trame UDP recus de : ");
    Serial.print(" IP Adresse : ");
    Serial.println(Udp.remoteIP());
    Serial.print(" Taille : ");
    Serial.println(packetSize);
    Serial.print(" Donnees : ");
    Serial.println(packetBuffer);
    // udp_Ex = 1;

    String s = String(packetBuffer);
    s.trim();
    s.toLowerCase();
    char consfg[14];
    for (int i = 0; i < consConfig.length(); i++)
    {
      consfg[i] = consConfig.charAt(i);
    }
    int consFlag = 0;
    // commandes UDP interface UDP
    if (s == "none")
    {
      udp_Ex = 0; /*consConfig ="00000000000000";*/
    }             // commande interface ARTH
    else if (s == "stopudp ")
    {
      udp_Ex = 0;
      ReplyBuffer = "Fin de la communication avec INISAT 2U ";
    }
    else if (s == "beginudp")
    {
      udp_Ex = 1;
      ReplyBuffer = "Client enregistre, debut de la communication avec INISAT 2U";
    }
    else if (s == "state")
    { /*consConfig = "state" ;*/
      ReplyBuffer = getState();
    } // A la requete "state" repondre au format CameraON|LoraON|Capteur9ON|Periode // commande interface ARTH
    else if (s == "cameraon")
    { // commande interface ARTH
      CamStatus = 1;
      digitalWrite(CAM_STATUT, CamStatus);
      Serial.println("... Camera activee ...");
      ReplyBuffer = getState();
    }
    else if (s == "cameraoff")
    { // commande interface ARTH
      CamStatus = 0;
      digitalWrite(CAM_STATUT, CamStatus);
      Serial.println("... Camera desactivee ...");
      ReplyBuffer = getState();
    }
    else if (s == "loraon")
    { // commande interface ARTH + standard
      LoraStatus = 1;
      if (loraOk == 1)
      {
        digitalWrite(LORA_LED, LoraStatus);
        Serial.println("... Liaison LORA Activee ...");
      } // LED LIAISON LORA
      ReplyBuffer = getState();
    }
    else if (s == "loraoff")
    { // commande interface ARTH + standard
      LoraStatus = 0;
      if (loraOk == 1)
      {
        digitalWrite(LORA_LED, LoraStatus);
        Serial.println("... Liaison LORA Desactivee ...");
      } // LED LIAISON LORA

      ReplyBuffer = getState();
    }
    else if (s == "test")
    {
      Serial1.flush();
      Serial1.print('A');
      autoTesting = 1;
      Serial.println("A");
      ReplyBuffer = getState();
    } // commande interface ARTH
    else if (s == "autotest")
    {
      Serial1.flush();
      Serial1.print('A');
      autoTesting = 1;
      Serial.println("A");
      ReplyBuffer = "Config " + s + " lancee ..";
    }
    else if (s == "gnsson")
    {               // commande interface ARTH
      modeGnss = 1; // variable utilise pour lancer le mode Releve de trajectoire GNSS
      modeGnss_start = millis();
      Serial1.flush();
      consConfig = "00000000000000";
      chart1 = '0';
      chart2 = '0';
      chart3 = '0';
      chart4 = '0';
      chart5 = '0';
      chart6 = '0';
      File file = SPIFFS.open("/Trajectoire_GNSS.txt", "w");
      if (!file)
      {
        Serial.println(" Failed to open Trajectoire_GNSS file for save");
        return;
      }
      else
      {
        //  file.println(inputMessage); file.println(" "); file.close();
        Serial.println(" Commande GNSS recue et fichier .txt cree ... ");
      }
      ReplyBuffer = getState();
    }
    else if (s == "gnssoff")
    {
      modeGnss = 2;
      ;
      ReplyBuffer = getState();
    } // commande interface ARTH
    else if (s == "gnsssave")
    {
      modeGnss = 0;
      fileTx();
      ReplyBuffer = getState();
    } // commande interface ARTH

    // Commandes UDP brutes <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    else if (s == "epson")
    {
      consfg[0] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "epsoff")
    {
      consfg[0] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "mplon")
    {
      consfg[1] = '1';
      consFlag = 1;
      consfg[2] = '1';
      consfg[3] = '1';
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "mploff")
    {
      consfg[1] = '0';
      consFlag = 1;
      consfg[2] = '0';
      consfg[3] = '0';
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "tempon")
    {
      consfg[1] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "tempoff")
    {
      consfg[1] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "alton")
    {
      consfg[2] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "altoff")
    {
      consfg[2] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "preson")
    {
      consfg[3] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "presoff")
    {
      consfg[3] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "bnoon")
    {
      consfg[4] = '1';
      consfg[5] = '1';
      consfg[6] = '1';
      consfg[7] = '1';
      consfg[8] = '1';
      consfg[9] = '1';
      consfg[10] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "bnooff")
    {
      consfg[4] = '0';
      consfg[5] = '0';
      consfg[6] = '0';
      consfg[7] = '0';
      consfg[8] = '0';
      consfg[9] = '0';
      consfg[10] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "euleron")
    {
      consfg[4] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "euleroff")
    {
      consfg[4] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "quaton")
    {
      consfg[5] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "quatoff")
    {
      consfg[5] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "vangon")
    {
      consfg[6] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "vangoff")
    {
      consfg[6] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "accon")
    {
      consfg[7] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "accoff")
    {
      consfg[7] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "magon")
    {
      consfg[8] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "magoff")
    {
      consfg[8] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "acclnon")
    {
      consfg[9] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "acclnoff")
    {
      consfg[9] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "gravon")
    {
      consfg[10] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "gravoff")
    {
      consfg[10] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "lumion")
    {
      consfg[11] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "lumioff")
    {
      consfg[11] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "locon")
    {
      consfg[12] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "locoff")
    {
      consfg[12] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "nmeaon")
    {
      consfg[13] = '1';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "nmeaoff")
    {
      consfg[13] = '0';
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "allon")
    {
      for (int i = 0; i < consConfig.length(); i++)
      {
        consfg[i] = '1';
      };
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    } // consfg=['1','1','1','1','1','1','1','1','1','1','1','1','1','1']
    else if (s == "alloff")
    {
      for (int i = 0; i < consConfig.length(); i++)
      {
        consfg[i] = '0';
      };
      consFlag = 1;
      ReplyBuffer = "Config " + s + " recue ..";
    } // consfg=['0','0','0','0','0','0','0','0','0','0','0','0','0','0'];
    else if (s == "lorastate")
    {
      if (LoraStatus == 1)
      {
        ReplyBuffer = "Etat LORA est : ON";
      }
      else
      {
        ReplyBuffer = "Etat LORA est : OFF";
      }
    }
    else if (s == "camstate")
    {
      if (CamStatus == 1)
      {
        ReplyBuffer = "Etat CAM est : ON";
      }
      else
      {
        ReplyBuffer = "Etat CAM est : OFF";
      }
    }

    else if (s == "dmagon")
    {
      demag = 1;
      ReplyBuffer = "Config " + s + " recue, veuillez attendre la fin ..";
    }
    else if (s == "magt1")
    { /*testmg = 1*/
      ;
      ReplyBuffer = "Config " + s + " recue .. COMMANDE DESACTIVEE POUR L'INSTANT ..";
    }
    else if (s == "magt2")
    { /*testmg = 2*/
      ;
      ReplyBuffer = "Config " + s + " recue .. COMMANDE DESACTIVEE POUR L'INSTANT ..";
    }
    else if (s == "magt3")
    { /*testmg = 3*/
      ;
      ReplyBuffer = "Config " + s + " recue .. COMMANDE DESACTIVEE POUR L'INSTANT ..";
    }
    else if (s == "magt4")
    { /*testmg = 4*/
      ;
      ReplyBuffer = "Config " + s + " recue .. COMMANDE DESACTIVEE POUR L'INSTANT ..";
    }
    else if (s == "stpmgt")
    {
      testmg = 0;
      ReplyBuffer = "Config " + s + " recue, veuillez attendre la fin ..";
    }

    else if (s == "help")
    {
      ReplyBuffer = ReplyBuffer + "  acclnOff :  Desactiver la supervision de l'Acceleration Lineaire \n";
      ReplyBuffer = ReplyBuffer + "  acclnOn : Activer la supervision de l'Acceleration Lineaire  \n";
      ReplyBuffer = ReplyBuffer + "  accOff :  Desactiver la supervision de l'Acceleration  \n";
      ReplyBuffer = ReplyBuffer + "  accOn : Activer la supervision de l'Acceleration \n";
      ReplyBuffer = ReplyBuffer + "  allOff :  Desactiver la supervision de l'ensemble des parametres \n";
      ReplyBuffer = ReplyBuffer + "  allOn : Activer la supervision de  l'ensemble des parametres  \n";
      ReplyBuffer = ReplyBuffer + "  altOff :  Desactiver la supervision de l'Altitude  \n";
      ReplyBuffer = ReplyBuffer + "  altOn : Activer la supervision de l'Altitude   \n";
      ReplyBuffer = ReplyBuffer + "  autoTest :  Lancer un Autotest  \n";
      ReplyBuffer = ReplyBuffer + "  beginUdp : Enregistrement du client et autorisation d’envoie des trames de données  \n";
      ReplyBuffer = ReplyBuffer + "  bnoOff :  Desactiver la supervision de l'ensemble des parametres renvoyes par le BNO  \n";
      ReplyBuffer = ReplyBuffer + "  bnoOn : Activer la supervision de  l'ensemble des parametres renvoyes par le BNO   \n";
      // ReplyBuffer = ReplyBuffer + "  camCapture :  Prendre une capture avec la Camera  \n";
      ReplyBuffer = ReplyBuffer + "  camOff :  Desactiver la Camera   \n";
      ReplyBuffer = ReplyBuffer + "  camOn : Activer la Camera  \n";
      ReplyBuffer = ReplyBuffer + "  camState :  Afficher l'etat de la Camera \n";
      // ReplyBuffer = ReplyBuffer + "  camStream : Demarrer un stream avec la Camera  \n";
      ReplyBuffer = ReplyBuffer + " dmagOn : Lancer une demagnetisation des magnetocoupleurs \n";
      ReplyBuffer = ReplyBuffer + "  epsOff :  Desactiver la supervision de l'ensemble des parametres de la carte EPS   \n";
      ReplyBuffer = ReplyBuffer + "  epsOn : Activer la supervision de  l'ensemble des parametres de la carte EPS  \n";
      ReplyBuffer = ReplyBuffer + "  eulerOff :  Desactiver la supervision de Vecteur d'Euler   \n";
      ReplyBuffer = ReplyBuffer + "  eulerOn : Activer la supervision de Vecteur d'Euler  \n";
      ReplyBuffer = ReplyBuffer + "  gravOff : Desactiver la supervision de Vecteur Gravite  \n";
      ReplyBuffer = ReplyBuffer + "  gravOn :  Activer la supervision de Vecteur Gravite  \n";
      ReplyBuffer = ReplyBuffer + "  help :  Afficher la liste des commandes existantes et leur explications  \n";
      ReplyBuffer = ReplyBuffer + "  locOff :  Activer la supervision de la localisation GNSS   \n";
      ReplyBuffer = ReplyBuffer + "  locOn : Desactiver la supervision de la localisation GNSS \n";
      ReplyBuffer = ReplyBuffer + "  loraOff : Desactiver la liaison LORA   \n";
      ReplyBuffer = ReplyBuffer + "  loraOn :  Activer la liaison LORA \n";
      ReplyBuffer = ReplyBuffer + "  loraState : Afficher l'etat de la liaison LORA   \n";
      ReplyBuffer = ReplyBuffer + "  lumiOff : Desactiver la supervision de la Luminance  \n";
      ReplyBuffer = ReplyBuffer + "  lumiOn :  Activer la supervision de la Luminance   \n";
      ReplyBuffer = ReplyBuffer + "  magOff :  Desactiver la supervision de Champs Magnetique  \n";
      ReplyBuffer = ReplyBuffer + "  magOn : Activer la supervision de Champs Magnetique  \n";
      ReplyBuffer = ReplyBuffer + "  magT1 : Lancer le test de rotation boussole par magnetocoupleurs N°1  \n";
      ReplyBuffer = ReplyBuffer + "  magT2 : Lancer le test de rotation boussole par magnetocoupleurs N°2  \n";
      ReplyBuffer = ReplyBuffer + "  magT3 : Lancer le test de rotation boussole par magnetocoupleurs N°3  \n";
      ReplyBuffer = ReplyBuffer + "  magT4 : Lancer le test de rotation boussole par magnetocoupleurs N°4  \n";
      ReplyBuffer = ReplyBuffer + "  mgRot+angle : Demarrer une rotation du satellite via les magnetocoupleurs, exp : mgRot+10, mgRot+-15 (en °)  \n";
      ReplyBuffer = ReplyBuffer + "  mplOff :  Desactiver la supervision de l'ensemble des parametres renvoyes par le MPL  \n";
      ReplyBuffer = ReplyBuffer + "  mplOn : Activer la supervision de  l'ensemble des parametres renvoyes par le MPL   \n";
      ReplyBuffer = ReplyBuffer + "  nmeaOff : Desactiver la supervision de la trame GNSS-NMEA  \n";
      ReplyBuffer = ReplyBuffer + "  nmeaOn :  Activer la supervision de la trame GNSS-NMEA   \n";
      ReplyBuffer = ReplyBuffer + "  presOff : Desactiver la supervision de la Pression  \n";
      ReplyBuffer = ReplyBuffer + "  presOn :  Activer la supervision de la Pression  \n";
      ReplyBuffer = ReplyBuffer + "  quatOff : Desactiver la supervision de la quaternion   \n";
      ReplyBuffer = ReplyBuffer + "  quatOn :  Activer la supervision de la quaternion  \n";
      ReplyBuffer = ReplyBuffer + "  riRot+sens+vitesse :  Demarrer une rotation de la roue a inertie, exp : riRot+a+40  (en %)  \n";
      // ReplyBuffer = ReplyBuffer + "  sCons : Sauvegarder toutes les donnees de la console dans un fichier .txt  \n";
      ReplyBuffer = ReplyBuffer + "  tCons+periode : Modifier de periode de reception des donnees sur la liaison UDP, exp tCons+10  (en secondes)   \n";
      ReplyBuffer = ReplyBuffer + "  stopUdp  : Fin de la communication UDP avec le satellite  \n";
      ReplyBuffer = ReplyBuffer + "  stpmgT : Arrêter le test magnetocoupleurs en cours  \n";
      ReplyBuffer = ReplyBuffer + "  tempOff : Desactiver la supervision de la Tempetarure  \n";
      ReplyBuffer = ReplyBuffer + "  tempOn :  Activer la supervision de la Tempetarure   \n";
      ReplyBuffer = ReplyBuffer + "  vangOff : Desactiver la supervision de la Vitesse Angulaire  \n";
      ReplyBuffer = ReplyBuffer + "  vangOn :  Activer la supervision de la Vitesse Angulaire   \n";

      ReplyBuffer = ReplyBuffer + "  Remarque : la saisie des commandes n'est pas sensible a la casse. \n";
    }
    else if (s == "camon")
    {
      CamStatus = 1;
      digitalWrite(CAM_STATUT, CamStatus);
      Serial.println("... Camera activee ...");
      ReplyBuffer = "Config " + s + " recue ..";
    }
    else if (s == "camoff")
    {
      CamStatus = 0;
      digitalWrite(CAM_STATUT, CamStatus);
      Serial.println("... Camera desactivee ...");
      ReplyBuffer = "Config " + s + " recue ..";
    }

    //********************
    else if (s.substring(0, 5) == "tcons")
    { // pereode de la console
      ReplyBuffer = "Commande ERROR !";
      if (s.substring(5, 6) == "+")
      {

        String TT2 = s.substring(6);
        if (isNumeric(TT2))
        {
          int TT = (atoi(String(s.substring(6)).c_str()));
          if ((TT > 4) && (TT < 3601))
          {
            console_intv = TT * 1000;
            ReplyBuffer = "Config " + s + " recue ..";
          }
          else
          {
            ReplyBuffer = "Veuillez choisir une periode entre 5 et 3600 secondes !";
          }
        }
        else
        {
          ReplyBuffer = "Veuillez choisir une periode entre 5 et 3600 secondes !";
        }
      }
    }
    //**************************
    else if (s.substring(0, 5) == "rirot")
    { // Roue a inertie
      ReplyBuffer = "Commande ERROR !";
      if ((s.substring(5, 6) == "+") && (s.substring(7, 8) == "+"))
      {
        if ((s.substring(6, 7) != "a") && (s.substring(6, 7) != "h"))
        {
          ReplyBuffer = "Veuillez choisir A ou H pour le Sens de rotation !";
        }
        else
        {
          String sd1 = s.substring(8);
          if (isNumeric(sd1))
          {
            int sd = atoi((s.substring(8)).c_str());
            Serial.println(sd);
            if ((sd < 0) || (sd > 100))
            {
              ReplyBuffer = "Veuillez choisir une valeur entre 0 et 100 % !";
            }
            else
            {
              int sens;
              int VITESSE = 255;
              if (s.substring(6, 7) == "h")
              {
                sens = 0;
              }
              else
              {
                sens = 1;
              }
              /*
              int vitesse2;
              if (sd>=50){ vitesse2 = map(sd, 50, 100, 12, 100);}
                else vitesse2 = map(sd, 0, 50, 0, 12);
              */

              VITESSE = map(sd, 100, 0, 0, 255);

              ledcWrite(ChannelX, 255);     // ouvrir le transistor P (vitesse nulle)avant le changement du sens pour proteger contre un court circuit eventuel
              digitalWrite(sensPin, sens);  // changement du sens de rotation pin 25
              ledcWrite(ChannelX, VITESSE); // changement de la vitesse de rotation via rapport cyclique pwm pin 23
              Serial.print("Commande recue pour (R.cyclique): " + String(255 - VITESSE) + " ,sense :" + String(s.charAt(1)));
              ReplyBuffer = "Config " + s + " recue ..";
            }
          }
          else
          {
            ReplyBuffer = "Veuillez choisir une valeur entre 0 et 100 % !";
          }
        }
      }
    }
    //*******************************************
    else if (s.substring(0, 5) == "mgrot")
    {
      ReplyBuffer = "Commande ERROR !";
      if (s.substring(5, 6) == "+")
      {
        String TT = s.substring(6);
        if (isNumeric(TT))
        {
          angRotCoup = atoi((s.substring(6)).c_str());
          if ((angRotCoup < -30) || (angRotCoup > 30) || (angRotCoup == 0))
          {
            ReplyBuffer = "Veuillez choisir une valeur entre -30 et 30° (et != 0) !";
          }
          else
          {
            Serial.println("Commande Magnetocoupleur recue pour: " + String(angRotCoup) + "°");
            float Bx = atoi((var24).c_str());
            float By = atoi((var25).c_str());
            float angB = round(atan2(By, Bx) * 180 / 3.14159265);
            float angTot = angB - angRotCoup;
            if (angTot > 360)
            {
              angTot = angTot - 360;
            }
            if (angTot < -360)
            {
              angTot = angTot + 360;
            }
            float ix = cos(angTot * 3.14159265 / 180);
            float iy = sin(angTot * 3.14159265 / 180);
            int sensX, sensY;
            if (ix > 0)
            {
              sensX = 0;
            }
            else
              sensX = 1;
            if (iy > 0)
            {
              sensY = 0;
            }
            else
              sensY = 1;

            int Ix = map(abs(ix * 100), 100, 0, 150, 255);
            int Iy = map(abs(iy * 100), 100, 0, 150, 255);

            digitalWrite(sensPin, sensX); // changement du sens du courant pin 25
            ledcWrite(ChannelX, Ix);      // changement de l'intensite du courant via le rapport cyclique pwm pin 23

            digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33
            ledcWrite(ChannelY, Iy);       // changement de l'intensite du courant via le rapport cyclique pwm pin 32

            String inputMessage = "Commande recue pour : " + String(angRotCoup) + "°.";
            Serial.println(inputMessage);
            ReplyBuffer = "Config " + s + " recue ..";
          }
        }
        else
        {
          ReplyBuffer = "Veuillez choisir une valeur entre -30 et 30° (et != 0) !";
        }
      }
    }
    //*************************
    // Commandes UDP interface JV uniquement (temps console, roue a inertie, magnetocoupleut) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    else if (s.charAt(0) == 't') // commande interface ARTH
    {
      ReplyBuffer = "Commande ERROR !";
      String TT2 = s.substring(1);
      if (isNumeric(TT2))
      {
        int TT = (atoi(String(s.substring(1)).c_str()));
        if ((TT > 4) && (TT < 3601))
        {
          console_intv = TT * 1000;
          ReplyBuffer = getState();
        }
        else
        {
          ReplyBuffer = "Veuillez choisir une periode entre 5 et 3600 secondes !";
        }
      }
    }
    else if (s.charAt(0) == 'r')
    { // commande interface ARTH
      ReplyBuffer = "Commande ERROR !";
      if ((s.charAt(1) != 'a') && (s.charAt(1) != 'h'))
      {
        ReplyBuffer = "Veuillez choisir A ou H pour le Sens de rotation !";
      }
      else
      {
        int sens;
        int VITESSE = 255;
        if (s.charAt(1) == 'h')
        {
          sens = 0;
        }
        else
        {
          sens = 1;
        }
        String VV = s.substring(2);
        if (isNumeric(VV))
        {
          int vitesse = atoi((s.substring(2)).c_str());
          Serial.println(vitesse);
          if ((vitesse > -1) && (vitesse < 101))
          {
            VITESSE = map(vitesse, 100, 0, 0, 255);

            ledcWrite(ChannelX, 255);     // ouvrir le transistor P (vitesse nulle)avant le changement du sens pour proteger contre un court circuit eventuel
            digitalWrite(sensPin, sens);  // changement du sens de rotation pin 25
            ledcWrite(ChannelX, VITESSE); // changement de la vitesse de rotation via rapport cyclique pwm pin 23
            Serial.print("Commande recue pour (R.cyclique): " + String(255 - VITESSE) + " ,sense :" + String(s.charAt(1)));
            ReplyBuffer = getState();
          }
          else
          {
            ReplyBuffer = "Veuillez choisir une valeur entre 0 et 100 % !";
          }
        }
        else
        {
          ReplyBuffer = "Veuillez choisir une valeur entre 0 et 100 % !";
        }
      }
    }
    else if (s.charAt(0) == 'm')
    { // commande interface ARTH
      ReplyBuffer = "Commande ERROR !";
      String CC = s.substring(1);
      if (isNumeric(CC))
      {
        angRotCoup = atoi((s.substring(1)).c_str());
        if ((angRotCoup > -30) && (angRotCoup < 30) && (angRotCoup != 0))
        {
          Serial.println("Commande Magnetocoupleur recue pour: " + String(angRotCoup) + "°");
          float Bx = atoi((var24).c_str());
          float By = atoi((var25).c_str());
          float angB = round(atan2(By, Bx) * 180 / 3.14159265);
          float angTot = angB - angRotCoup;
          if (angTot > 360)
          {
            angTot = angTot - 360;
          }
          if (angTot < -360)
          {
            angTot = angTot + 360;
          }
          float ix = cos(angTot * 3.14159265 / 180);
          float iy = sin(angTot * 3.14159265 / 180);
          int sensX, sensY;
          if (ix > 0)
          {
            sensX = 0;
          }
          else
            sensX = 1;
          if (iy > 0)
          {
            sensY = 0;
          }
          else
            sensY = 1;

          int Ix = map(abs(ix * 100), 100, 0, 150, 255);
          int Iy = map(abs(iy * 100), 100, 0, 150, 255);

          digitalWrite(sensPin, sensX); // changement du sens du courant pin 25
          ledcWrite(ChannelX, Ix);      // changement de l'intensite du courant via le rapport cyclique pwm pin 23

          digitalWrite(sensPinY, sensY); // changement du sens du courant pin 33
          ledcWrite(ChannelY, Iy);       // changement de l'intensite du courant via le rapport cyclique pwm pin 32

          String inputMessage = "Commande recue pour : " + String(angRotCoup) + "°.";
          Serial.println(inputMessage);
          ReplyBuffer = getState();
        }
      }
      else
      {
        ReplyBuffer = "Veuillez choisir une valeur entre -30 et 30° !";
      }
    }
    // Requete de changement de données console ARTH
    else if (s.length() == 14) // commande interface ARTH
    {
      int verif = 0;
      for (int i = 0; i < consConfig.length(); i++)
      {
        if ((s.charAt(i) != '1') && (s.charAt(i) != '0'))
        {
          verif = 1;
        }
      }

      if (verif == 0)
      {
        consConfig = s;
        ReplyBuffer = "Config console recue ..";
      }
      else
      {
        ReplyBuffer = "Commande ERROR !";
      }
    }
    // fin interface JV <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    // Requete inconnue
    else
      ReplyBuffer = "Commande ERROR !";

    if (consFlag == 1)
    {
      consConfig = String(consfg[0]) + String(consfg[1]) + String(consfg[2]) + String(consfg[3]) + String(consfg[4]) + String(consfg[5]) + String(consfg[6]) + String(consfg[7]) + String(consfg[8]) + String(consfg[9]) + String(consfg[10]) + String(consfg[11]) + String(consfg[12]) + String(consfg[13]);
      Serial.println(consFlag);
      Serial.println(consConfig);
      consFlag = 0;
    }

    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.printf(ReplyBuffer.c_str());
    Udp.printf("\r\n");
    Udp.endPacket();
    ReplyBuffer = "";
  } // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
}
// FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP FIN-LOOP
