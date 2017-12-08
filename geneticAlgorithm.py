# -*- coding: utf-8 -*-
# Python3.4*

import sys, subprocess, copy, random, pickle
import numpy as np
'''
This is a genentic algorithm to tune the weights in my scoring function
The code creates weights and has games randomly play against eachother
The fitness function is looking for the highest score.
The code is slow with large populations, but works.
'''
class GenAlgTuner:
	def __init__(self):
		self.n=6
		self.weightScoreList=[]
		self.population=[]


	def singleRun(self):
		l=len(self.population)
		halfL=int(l/2)
		#print(halfL)
		randomOrder=self.population[:]
		np.random.shuffle(randomOrder)
		wsList=[]
		front=randomOrder[:halfL]
		back=randomOrder[halfL:]
		f=open("scoreWeights.txt",'a')
		for i in range(halfL):
			playerA=front[i]
			playerB=back[i]
			tempList=[playerA,playerB]
			argDict1=self.createOneWeightDict(playerA[:])
			argDict2=self.createOneWeightDict(playerB[:])
			self.callBotBattle(argDict1,argDict2)
			points, winner=self.fitness()
			print(points)
			winInd=0
			if winner=="player2":
				winInd=1
			f.write(str(points)+", "+str(tempList[winInd])+"\n")
			wsList.append((points,tempList[:],winInd))
		f.close()
		self.weightScoreList=sorted(wsList[:], reverse=True)
		return 

	def swap(self,arglist1,arglist2,rate=.05):
		if random.random()>(1-rate):
			l=self.n
			new1=arglist2[:l]+arglist1[l:]
			new2=arglist1[:l]+arglist2[l:]
			return new1[:], new2[:]
		else:
			return arglist1[:], arglist2[:]

	def nextIteration(self):
		tempList=[]
		l=len(self.weightScoreList[:])
		#h=int(l/2)
		front=self.weightScoreList[:l]
		for i in range(l):
			l1=front[i][1][front[i][2]]
			l2=front[i][1][front[i][2]]
			n1, n2= self.swap(l1,l2)
			n1=self.change(n1[:])
			n2=self.change(n2[:])
			tempList.append(n1)
			tempList.append(n2)
		self.population=tempList[:]
		return

	def change(self,weightList):
		a=-1.0
		for i in range(len(weightList)):
			if i==3:
				a=a*a
			if random.random()>.95:
				weightList[i]=random.random()*a
		return weightList[:]


'''
	callBotBattle creates a shell script that creates two instances of the blockBattle engine and
	assigns random weights to each bot to compete against eachother. This function creates a new file and executes
	the script each time it is run.

'''
			

	def callBotBattle(self, arglist1={'ah':-.5,'cl':1,'h':-.9,'bump':-.3,'c2o':2,'c4o':1},arglist2={'ah':-.5,'cl':1,'h':-.9,'bump':-.3,'c2o':2,'c4o':1}):
		script=open("runScript.sh",'w+')
		callString='#!/bin/sh'
		callString=callString+'\n'
		callString=callString+'\n'
		callString=callString+'cd /Users/nugthug/Documents/cmpsci/383/final/blockbattle-engine-master/'
		callString=callString+'\n'
		callString=callString+'java -cp bin com.theaigames.blockbattle.Blockbattle '
		callString=callString+'"python3 /Users/nugthug/Documents/cmpsci/383/final/starter_py3_converted/BotRunArgs.py '
		callString=callString+str(arglist1['ah'])+' '+str(arglist1['cl'])+' '+str(arglist1['h'])+' '+str(arglist1['bump'])+' '+str(arglist1['c2o'])+' '+str(arglist1['c4o'])+'" '
		callString=callString+'"python3 /Users/nugthug/Documents/cmpsci/383/final/starter_py3_converted/BotRunArgs.py '
		callString=callString+str(arglist2['ah'])+' '+str(arglist2['cl'])+' '+str(arglist2['h'])+' '+str(arglist2['bump'])+' '+str(arglist2['c2o'])+' '+str(arglist2['c4o'])+'" '
		callString=callString+"2>err.txt 1>out.txt"
		#subprocess.call("./callJavaBot.sh",shell=False)
		script.write(callString)
		script.close()
		subprocess.call("./runScript.sh",shell=False)

	def getMaxScore(self):
		path="/Users/nugthug/Documents/cmpsci/383/final/blockbattle-engine-master/out.txt"
		f=open(path,'r+')
		maxRowPoints=0
		maxRound=0
		maxCombo=0
		maxSkips=0
		winner=""
		for line in f:
			wordList=line.strip('\n').split()
			if len(wordList)>0:
				if wordList[0]=='Round':
					maxRound=int(wordList[1])
				if len(wordList)==4:
					if wordList[2]=='row_points':
						if int(wordList[3])>maxRowPoints:
							maxRowPoints=int(wordList[3])
							winner=wordList[1]
					if wordList[2]=='combo':
						maxCombo=max(maxCombo,int(wordList[3]))
					if wordList[2]=='skips':
						maxSkips=max(maxSkips,int(wordList[3]))
		f.close()
		return maxRound, maxRowPoints, maxCombo, maxSkips, winner

	def fitness(self):
		rounds, points, combo, skip, winner=self.getMaxScore()
		return points, winner

	def createOneWeightDict(self,weights):
		keys=['ah','h','bump','cl','c2o','c4o']
		return dict(zip(keys,weights))

	def createWeights(self):
		a=-1.0
		weights=[]
		for i in range(self.n):
			if i==3:
				a=a*a
			score=random.random()*a
			weights.append(score)
		return weights[:]

	def popInit(self,n):
		tempList=[]
		for i in range(n):
			w=self.createWeights()
			tempList.append(w)
		self.population=tempList[:]
		return

	def runItAll(self,popsize=1000,episodes=10000):
		f=open("scoreWeightsTop.txt",'w')
		self.popInit(popsize)
		for i in range(episodes):
			print("Starting")
			self.singleRun()
			if len(self.weightScoreList)>0:
				topScore, bestWeights, winInd=self.weightScoreList[0]
				print(str(i+1)+": TopScore: "+str(topScore)+" BestWeights: "+str(bestWeights[winInd]))
				f.write(str(topScore)+", "+str(bestWeights[winInd])+"\n")
			self.nextIteration()
		f.close()






			




	# def singleRound(self,numRounds):
	# 	for i in range(numRuns)
if __name__=='__main__':
	test=GenAlgTuner()
	test.runItAll(100,100)
	# test.callBotBattle()
	# rounds,rows,combo,skips=test.getMaxScore()
	# print("Rounds: "+str(rounds))
	# print("Row Score: "+str(rows))
	# print("Combos: "+str(combo))
	# print("Skips: "+str(skips))
