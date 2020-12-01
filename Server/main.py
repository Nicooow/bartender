# -*- coding: utf-8 -*-

from py import serverWs
import time

def message_received(client, server, message):
    print("> " + str(message))
    args = message.split("|")
    fnct = args[0]
    print(args)
    if(fnct=="ask"):
        if(args[1] == "cuves"):
            serverRs.server.send_message(client, "addElement|cuve|1|Coca|#8A4C15|120")
            serverRs.server.send_message(client, "addElement|cuve|2|Orange|#FF8000|40")
            serverRs.server.send_message(client, "addElement|cuve|3|Vodka|#E4E4E4|70")
            serverRs.server.send_message(client, "addElement|cuve|4|Whisky|#521E1E|110")
            serverRs.server.send_message(client, "addElement|cuve|5|Get27|#06AF06|20")
            serverRs.server.send_message(client, "addElement|cuve|6|Eau|#0FA4F9|50")
            serverRs.server.send_message(client, "animation|cuves")
        elif(args[1] == "boissons"):
            serverRs.server.send_message(client, "addElement|boisson|Coca|https://stock.flashmode.tn/wp-content/uploads/2020/06/coca-cola-logo-png-100.png|#FF8000|0")
            serverRs.server.send_message(client, "addElement|boisson|Jagermeister|https://lezebre.lu/images/detailed/16/22045-jagermeister-logo.png|#FF8000|35")
            serverRs.server.send_message(client, "addElement|boisson|Ice-Tea|https://freevectorlogo.net/wp-content/uploads/2013/03/ice-tea-lipton-vector-logo.png|#FF8000|0")
            serverRs.server.send_message(client, "addElement|boisson|Redbull|https://cdn.freebiesupply.com/logos/large/2x/red-bull-logo-png-transparent.png|#FF8000|0")
            serverRs.server.send_message(client, "addElement|boisson|Orangina|https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRam3ARjr4sPdKgDNZpHICoy6VlxvpFelx-Jw&usqp=CAU|#FF8000|0")
            serverRs.server.send_message(client, "addElement|boisson|Clan Campbell|https://media.discordapp.net/attachments/328323448923488259/756193312435601549/clancampbell.png|#FF8000|40")

serverRs = serverWs.serverWs()
serverRs.fn_message_received = message_received
serverRs.start()

while 1:
    mot = input()
    if(mot=="stop"):
        serverRs.server.shutdown()
        break
    serverRs.server.send_message_to_all(mot)
