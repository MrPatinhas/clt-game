This is a game description file. The game name is CLT (Cartola Legends of Time). The architecture is a roguelike game in which a player will leverage its memory knowledge of past performances from the famous game of Cartola FC - fantasy soccer game about Campeonato Brasileiro. The idea is that the player will have a fixed rooster of players to compete against the AI. However each round the YEAR and ROUND of the championship will change so a player A that was amazing in 2023 can be not so good in a match in 2014, nor even thvae played that round …
The goals is for the game to be played in the browser so HTML + [node.js](http://node.js) should suffice but I am very opened to architecture decision discussions.
DATA ECOSYSTEM
We have already builted an python script to assemble the core databases for the project a full handover file is provided. A player score is defined by the sum of a set of scouts. There is a catch for us to handle after. Some scouts changed over time
DD (Defesa dificil) became DE
RB (Roubada de Bola) became DS
and PE (Passe errado) was erased. Also new ones such as PS (Penalti sofrido) was reintroduced
Lets create a conversion factor for DD -> DE and RB → DS. The we add this disclaimer that in order to normalized DD and RB were converted to DS by factors
PE, PS or other scouts that were extinct or created without a direct match can be excluded
The scout weight are:
Positive Scouts (Ações Positivas)
Gol (G): +8,0 pontos
Assistência (A): +5,0 pontos
Jogo sem sofrer gols (SG - exclusivo para defensores/goleiros): +5,0 pontos
Defesa de pênalti (DP - exclusivo para goleiro): +7,0 pontos
Defesa difícil (DD - exclusivo para goleiro): +3,0 pontos
Defesa simples (DE - exclusivo para goleiro): +1,3 ponto
Desarme (DS): +1 ponto
Roubada de Bola (RB): 1.5
Finalização na trave (FT): +3,0 pontos
Finalização defendida (FD): +1,2 ponto
Finalização para fora (FF): +0,8 ponto
Pênalti sofrido (PS): +1,0 ponto
Falta sofrida (FS): +0,5 ponto [[1](https://ge.globo.com/cartola/noticia/2025/03/17/quanto-vale-a-pontuacao-de-cada-scout-no-cartola.ghtml),[2](https://cartolafcmix.com/arquivo-mix/duvidas-frequentes-sobre-o-cartola-fc-2/)]
Negative Scouts (Ações Negativas)
Gol contra (GC): -3,0 pontos
Cartão vermelho (CV): -3,0 pontos
Cartão amarelo (CA): -1,0 ponto
Gol sofrido (GS - exclusivo para goleiro): -1,0 ponto
Pênalti cometido (PC): -1,0 ponto
Falta cometida (FC): -0,3 ponto
Impedimento (I): -0,1 ponto
Passe incompleto (PI/PE): -0,1 ponto
Pênalti perdido: -4
The game will have the following mechanics
STAGE 1 - THE BARN AND THE ROOSTERS
Rooster selections. We will create 7 pre-defined roosters. In order to maximize player appearances throughou all the years the roosters will have the top N players which best matches appearances and average score, thus providing a good baseline. Cartola FC has a component to choose from that is the FORMATION therefore we need to provide within the rooster a specific amount of players by position. It will be apparent that some players change position in the years, in order to fill the rooster we will consider the MOST COMMON POSITION played, so if a player was MEI (midfield) in 90 games and ATA (stricker) in 10 games we will sample as one of the MEI. The roosters must have
2 GKS (2 GOL - 2 goalkeepers)
4 ZAG (2 linebackers)
4 LAT (2 Sideplayers)
8 MEI (8 midfielders)
5 ATA (5 strikers)
1 TEC (1 coach)
The rooster card should be appealing with a good aesthetic. The cards should be by line
Player short name
Player position
Player teams (here we sample the top 3 played) if possible we add the logo of the teams if not we just select the teams short name like COR, CRU, SPO for a player that played in corinthians Cruzeiro and São Paulo
Avg Score throught the years
Number of rounds played
If possible: Miniature with player image (if url present on database) if not we can use standart placeholder images
I would like the cards to be in a carousel so the player can browse throught them using the click to circle the carousel or arrow keys, the carousel should be in perspective so the current cars is more visible and the adjacent one in an angle
Once the player select their rooster the AI can only choose from the other roosters to be fair and avoid same player athelte in opposite sides. After choosing the AI and human player cards should be in a minimized window that when clicked can be consulted in any point of the game
STAGE 2 - PARAMETERS
In this stage we will set the parameters of the game (Which Round and Which Year) one player chooses the round of the championship and the other the year. The game will have best of 5 rounds, in each rounds it alternates who chooses what (round of championship or year)
STAGE 3 - BUCKET OF THE SOULS
Since the year selection and the round can make a player not play therefore score = 0 we will provide a help for the player and give a selection of 6 names one for each position that we now for sure from the database that played in that given ROUND-YEAR parameter. The human player and the AI can then choose if it wants to remove someone from its rooster and add this new sould.
IMPORTANT: We can say which team the player was defending but we can not say what is the average score nor nothing that would hint its performance.
Once choosen the player will have dropped someone origninally from its rooster and therefore will only be able to be picked up in another bucet of souls if it appears (or other game steps we can add)
IMPORTANT: The 6 names that will appear can not be already in the roosters of the opponent.
IMPORTANT: The same 6 names will appear for both and the last one who choose the parameter will pick the sould bucket first. So for example
PLAYER A: chooses round
PLAYBER B: Chooses year
PLAYER A: Chooses first sould
Playerb B: chooses second soul
IMPORTANT: The player can drop the same position it is being harvest from the bucket, to to gather a new ATA needs to drop an ATA
important: A player can decide to pass and not use the bucket
STAGE 4 - HIGHLIGHTS OF DESTINY
Each round of brasileirao usually has 10 games (20 teams). In this stage we will show 5 horizontal bar in 2 columns all in gray. The player can then choose between two options
reveal 5 matchups
reveal 2 matchups and scores (home team score and away team score)
IMPORTANT: The player MUST CHOOSE ONE OF THE OPTIONS.
IMPORTANT: The revealed matchups are random
STAGE 5 - CRAZY RULE
In order to make the game less deterministic in this moment a crazy rule will be sorted out that will alter how the scouts are weighted in. Here are some in the first draft I made (I will like to add some more in the future)
Nome da Regra
Explicação
FS
PE
A
FT
FD
FF
G
I
PP
RB
FC
GC
CA
CV
SG
DD
DP
GS
Regra de Gabriel Jesus
Gol não vale nada. O que vale é marcar lateral e roubar bola
0.5
-0.3
5
3.5
0.6
0.4
4
-0.5
-3.5
4
-0.5
-6
-2
-5
5
3
7
-2
Regra de Felipe Melo
Cartão é sinal de entrega e não punição. Toda falta é simulação
-0.5
-0.3
5
3.5
1.2
0.8
8
-0.5
-3.5
1.7
0
-6
2
5
5
3
7
-2
Regra do Futsal
Passe é o fundamento mais importante. Sem Impedimentos
0.5
-0.8
5
3.5
1.2
0.8
8
0
-3.5
1.7
-0.5
-6
-2
-5
5
3
7
-2
Regra do Mano Menezes
Achei Ofensivo Recua. SG vale o Dobro
0.5
-0.3
5
3.5
1.2
0.8
8
-0.5
-3.5
1.7
-0.5
-6
-2
-5
10
3
7
-2
Regra do Vanderlei
O que vale na vida são Pontes. GS amplia e DD vale muito
0.5
-0.3
5
3.5
2
0.8
8
-0.5
-3.5
1.7
-0.5
-6
-2
-5
5
7
14
-4
Regra do Garçom
Mais vale aquele que compartilha que aquele que comemora
0.5
-0.6
10
3.5
1.2
0.8
5
-0.5
-3.5
1.7
-0.5
-6
-2
-5
5
3
7
-2
Regra do Buda
Seja positivo. Zero negatividades
0.5
0
5
3.5
1.2
0.8
8
0
0
1.7
0
0
0
0
5
3
7
0
Regra Open Capitão
DOBRO DE TUDO E QUADRUPLO DO RESTO
1
-1.2
10
7
2.4
1.6
16
-2
-14
3.4
-2
-24
-8
-20
10
6
14
-8
STAGE 6 - FIRST HALF
In this section and most straight forward each player will select the players to be in play. Important it need to be a valid formation among the following
1 GK - 2 ZAG - 2 LAT - 4 MEI - 2 ATA - 1 TEC
1 GK - 2 ZAG - 2 LAT - 3 MEI - 3 ATA - 1 TEC
1 GK - 2 ZAG - 2 LAT - 5 MEI - 1 ATA - 1 TEC
1 GK - 3 ZAG - 4 MEI - 3 ATA - 1 TEC
1 GK - 3 zag - 5 MEI - 2 ATA - 1 TEC
Visually speaking as the player selects its athlete it should be added to a mini-field, if a formation is invalid or a player is missing then there must be a red signal on the field signalignaling changes. If all good then a green one and a button saying KICK OFF for the simulation to run
IMPORTANT: The player must choose a captain, this players score will be doubled (both for good or bad)
STAGE 7 - HALF TIME
^^the simulation^^ is merely the application of the scout and the crazy weights to get the score, there isn't any fancy simulation, all deterministic. Here in the half time the player will have access to 2 information
Among 6 random athletes from each team who is winning and by how much. So for example player A will have among 6 random players 21 points and player B among 6 random in filed players 18. We will show: (Player A wins a random 6 sample by 21 vs 18)
With this info the player then decides if it wants to make a substitution, taking someone from the field and add someone remaining from the rooster. A formation CAN BE CHANGED however the maximum number of changes is 3 athletes
We will add some power-up cards in the future such as (REVEAL ZEROED PLAYERS) that can be used in one-off half time to highlight in neon blue who is zeroed.
Other power ups are:
COPYCAT: The player selects one adversarial athlete and one of their one and says the score of the player is the same of the adversarial (only for one player)
GRENAL: 3 random players are removed from each team
STAGE 8 - MATCH CONCLUSION
After the changes and the power-ups then we check which team on the field has the highest score. It is very important to show an analytical report with the score of each player for each team, the scouts (in an expandable way), the MVP and the score for the bench
—
STAGES 2 throught 8 correspond to a game, the first to win 3 games wins (we can create a mode with only 2 wins to set the winner, like a best of three)
IMPORTANT: When playing against the IA the next game the IA must choose a different rooster after the beginning
About the IA difficulty we can make it have some partial data to choose from like the player avg on all dataframe, player avg in that year's championship and the true score of the round in a more difficult match up. I would like us to have a multiplayer mode (note multi server side, but something, two people can alternate in same screen, however for now seems like the computer opponent is the best way to validate the idea)
—
Ways of working
After each step we analyze the app to see the functionalities for me to provide feedback
The FIRST THING you must do is devise a detailed and organized plan of implementation to be stored in a file and used as a worklog by the agents