# Gestion des EventsSource, côté serveur
## Gestion de la connexion
Maintenir la connexion TCP ouverte ! 
## Format de la réponse initiale (lors de la réception de la requête d'événement)
    HTTP/1.1 200 OK\r\n
    Cache-Control: no-cache\r\n
    Content-Type: text/event-stream\r\n\r\n
## Envoi d'un événement
    event: nom_de_l_evenement\n
    data: {\"value\":\"hellofromserver\"}\n\n
## Fermeture de la connexion
ERRNO:104 (ECONNRESET)
On peut gérer cette exception avec un 
    try: 
    
    except OSError as err:
            print("OSERROR:"+str(err.errno))
            if(err.errno==104):
                print("Connexion reset")
