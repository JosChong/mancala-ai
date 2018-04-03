# File: ycn498.py
# Author(s) names AND netid's: YoonSang Chong (ycn498)
# Date: October 16th, 2017
# Group work statement: <please type the group work statement
#      given in the pdf here>
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.

# IMPORTANT: written in Python3 then converted to Python2 syntax
# note the declaration of Player as a new-style class (child of object), necessary for the Custom Player's constructor

from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player(object):
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4

    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score

    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (turn.score(board), m)
            if board.gameOver():
                return (-1, -1)
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.alphaBetaMinValue(nb, ply-1, turn, score, INFINITY)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #returns the best score and the associated move
        return score, move

    def alphaBetaMaxValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation using alpha beta pruning. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        na = deepcopy(alpha)
        # Copy the alpha value so that we don't ruin it for previous nodes in our search tree
        for m in board.legalMoves(self):
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            #try the move
            score = max(score, opponent.alphaBetaMinValue(nextBoard, ply-1, turn, na, beta))
            #and see what the opponent would do next
            #if the result is better than our best score so far in this ply, save that score
            if score >= beta:
                #if our best score in this ply is worse for the opponent than their best guaranteed score so far
                #return the current score as the opponent will never allow the game to progress to this state anyway
                return score
            na = max(na, score)
            #if we come across a score better than our best score so far, set it equal to alpha
        #returns the best score from this ply
        return score

    def alphaBetaMinValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation using alpha beta pruning. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        nb = deepcopy(beta)
        # Copy the beta value so that we don't ruin it for previous nodes in our search tree
        for m in board.legalMoves(self):
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            #try the move
            score = min(score, opponent.alphaBetaMaxValue(nextBoard, ply-1, turn, alpha, nb))
            #and see what the opponent would do next
            #if the result is better than our best score so far in this ply, save that score
            if score <= alpha:
                #if our best score in this ply is worse for the opponent than their best guaranteed score so far
                #return the current score as the opponent will never allow the game to progress to this state anyway
                return score
            nb = min(nb, score)
            #if we come across a score better than our best score so far, set it equal to beta
        #returns the best score from this ply
        return score

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print (move, "is not valid")
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print ("chose move", move)
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print ("chose move", move, " with value", val)
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print ("chose move", move, " with value", val)
            return move
        elif self.type == self.CUSTOM:
            val, move = self.alphaBetaMove(board, self.ply)
            print ("chose move", move, " with value", val)
            return move
        else:
            print ("Unknown player type")
            return -1


# Custom Player
# IMPORTANT: uses super() in the constructor, so requires that the parent Player class be declared as a new-style class
# (child of object)
class ycn498(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def __init__(self, playerNum, playerType=Player.CUSTOM, ply=9):
        """Initialize a Custom Player with a playerNum (1 or 2), playerType (default is Player.CUSTOM), and a ply (default is 9)."""
        super(ycn498, self).__init__(playerNum, playerType, ply)

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ((board.getPlayersCups(self.num)[m-1] - (board.NCUPS-(m-1)))%13) == 0:
                #if this move will end in the Mancala, prioritize it
                return INFINITY, m
            #if (board.getPlayersCups(self.num)[m-1]%13) < (board.NCUPS-(m-1)) and board.getPlayersCups(self.num)[(board.getPlayersCups(self.num)[m-1]%13)+m-1] == 0:
                #if this move will end in an empty pit on the player's side, prioritize it
                #return INFINITY, m
                #commented out due to worse game performance
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (turn.score(board), m)
            if board.gameOver():
                return (-1, -1)
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = ycn498(self.opp)
            s = opp.alphaBetaMinValue(nb, ply-1, turn, score, INFINITY)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #returns the best score and the associated move
        return score, move

    def alphaBetaMaxValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation using alpha beta pruning. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        na = deepcopy(alpha)
        # Copy the alpha value so that we don't ruin it for previous nodes in our search tree
        for m in board.legalMoves(self):
            #if ((board.getPlayersCups(self.num)[m-1] - (board.NCUPS-(m-1)))%13) == 0:
                #if this move will end in the Mancala, prioritize it
                #return INFINITY
                #commented out due to worse game performance
            #if (board.getPlayersCups(self.num)[m-1]%13) < (board.NCUPS-(m-1)) and board.getPlayersCups(self.num)[(board.getPlayersCups(self.num)[m-1]%13)+m-1] == 0:
                #if this move will end in an empty pit on the player's side, prioritize it
                #return INFINITY
                #commented out due to worse game performance
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return turn.score(board)
            # make a new player to play the other side
            opponent = ycn498(self.opp)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            #try the move
            score = max(score, opponent.alphaBetaMinValue(nextBoard, ply-1, turn, na, beta))
            #and see what the opponent would do next
            #if the result is better than our best score so far in this ply, save that score
            if score >= beta:
                #if our best score in this ply is worse for the opponent than their best guaranteed score so far
                #return the current score as the opponent will never allow the game to progress to this state anyway
                return score
            na = max(na, score)
            #if we come across a score better than our best score so far, set it equal to alpha
        #returns the best score from this ply
        return score

    def alphaBetaMinValue(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation using alpha beta pruning. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        nb = deepcopy(beta)
        # Copy the beta value so that we don't ruin it for previous nodes in our search tree
        for m in board.legalMoves(self):
            #if ((board.getPlayersCups(self.num)[m-1] - (board.NCUPS-(m-1)))%13) == 0:
                #if this move will end in the Mancala, prioritize it
                #return -INFINITY
                #commented out due to worse game performance
            #if (board.getPlayersCups(self.num)[m-1]%13) < (board.NCUPS-(m-1)) and board.getPlayersCups(self.num)[(board.getPlayersCups(self.num)[m-1]%13)+m-1] == 0:
                #if this move will end in an empty pit on the player's side, prioritize it
                #return -INFINITY
                #commented out due to worse game performance
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return turn.score(board)
            # make a new player to play the other side
            opponent = ycn498(self.opp)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            #try the move
            score = min(score, opponent.alphaBetaMaxValue(nextBoard, ply-1, turn, alpha, nb))
            #and see what the opponent would do next
            #if the result is better than our best score so far in this ply, save that score
            if score <= alpha:
                #if our best score in this ply is worse for the opponent than their best guaranteed score so far
                #return the current score as the opponent will never allow the game to progress to this state anyway
                return score
            nb = min(nb, score)
            #if we come across a score better than our best score so far, set it equal to beta
        #returns the best score for this ply
        return score

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # although we are evaluating the board for a specific player, there is no guarantee that it will be that player's turn
        # so any specific moves available now may not be when the player's turn comes around
        # for that reason, the logic to prioritize moves that end in the Mancala or an empty pit has been implemented in
        # the alpha beta pruning algorithm used by the Custom Player instead of the board scoring function here
        # we rely on that logic and the nature of searching with plies (which, along with the board scoring function,
        # reflects the score gains of these advantageous moves) to guide our Custom Player
        # the following scoring mechanism works instead on rudimentary statistical principles of the Mancala game

        # for every stone in the player's Mancala, add one to the score
        # for every stone in the opponent's Mancala, subtract one from the score
        score = 0.0
        for s in range(board.scoreCups[self.num-1]):
            score += 1
        for s in range(board.scoreCups[self.opp-1]):
            score -= 1
        # regardless of where the stones are, every 6 stones on the player's side guarantees one stone in their Mancala,
        # unless the opponent steals them by landing in an empty spot on their side
        # for simplicitiy's sake, one is added to the score for every 6 stones on the player's side
        # and one is subtracted for every 6 stones on the opponent's side
        stones = 0.0
        cups = board.getPlayersCups(self.num)
        oppCups = board.getPlayersCups(self.opp)
        for c in range(board.NCUPS):
            stones += cups[c]
            stones -= oppCups[c]
        score += stones/(board.NCUPS)
        # warning: crude reasoning and likely not numerically significant in most cases
        # if an empty pit exists, there is a 1/13 chance that a pit with a random number of stones will finish in that empty pit
        # so, add (stones across the player's empty pits)/13 to the score, and subtract accordingly given the opponent's empty pits
        # note that we are ignoring the possibility that either player places stones into their opponent's empty pits,
        # thereby not allowing the opponent even a chance to reap the rewards
        stones = 0.0
        for c in range(board.NCUPS):
            if cups[c] == 0:
                stones += oppCups[board.NCUPS-c-1]
            if oppCups[c] == 0:
                stones -= cups[board.NCUPS-c-1]
        score += stones/(2*board.NCUPS+1)
        # return the board score
        return score

# in order to create a better Player/scoring algorithm, we could pass the Player whose turn it is at each ply down
# the search algorithm so that at the final ply, the scoring algorithm can use it to determine the state of the board
# for that specific player
# however, the current Custom Player has satisfactory game performance, and it seems that complicating its mechanisms has only
# served to weaken that performance, so this is not implemented
