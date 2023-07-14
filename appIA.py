from laberintoIA import *

""" import laberintos """
laberintoTxt = "./laberintos/laberinto1.txt"

""" Posibles algoritmos BFS DFS GBFS A* """

laberinto = Laberinto("GBFS", laberintoTxt).resolver()
