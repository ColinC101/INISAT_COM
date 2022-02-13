# Commandes
## Commandes avec graphique
    EPS => Etat du système électronique (Vbat, Icharge, TBat)  | Chart:'k' | Serial1:'B'
    TEMPERATURE => Température | Chart:'h' | Serial1:'C'
    ALT => Altitude | Chart:'i' | Serial1:'D'
    PRESS => Pression | Chart:'j' | Serial1:'E'
    EULER => Vecteur Euler | Chart:'a' | Serial1:'F'
    QUATERNION => Quaternion | Chart:'b' | Serial1:'G'
    V_ANG => Vitesse angulaire | Chart:'c' | Serial1:'H'
    ACC => Accélération | Chart:'d' | Serial1:'I'
    CHAMP_MAG => Champs magnétiques | Chart:'e' | Serial1:'J'
    ACC_LIN => Accélération linéaire | Chart:'f' | Serial1:'K'
    VEC_GRAV => Vecteur gravité | Chart:'g' | Serial1:'L'
    LUM => Luminance | Chart:'l' | Serial1:'M'

## Autres commandes
    GNSS => GNSS | Serial1:'N'
    NMEA => NMEA | Serial1:'O'

# Configuration console
    consConfig="00000000000000" (taille: 14 caractères)
    consConfig[x]=1 => Param x ON
    consConfig[x]=0 => Param x OFF

    consConfig[0] : EPS
    consConfig[1] : TEMPERATURE
    consConfig[2] : ALT
    consConfig[3] : PRESS
    consConfig[4] : EULER
    consConfig[5] : QUATERNION
    consConfig[6] : V_ANG
    consConfig[7] : ACC
    consConfig[8] : CHAMP_MAG
    consConfig[9] : ACC_LIN
    consConfig[10] : VEC_GRAV
    consConfig[11] : LUM
    consConfig[12] : GNSS
    consConfig[13] : NMEA
     
