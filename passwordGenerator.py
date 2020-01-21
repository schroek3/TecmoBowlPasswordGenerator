#Ken Schroeder
#01.20.2020
#Santa Cruz, CA
#Tecmo Bowl Password Generator

#----------imports--------------------------------------------------------------
import math
#-------------------------------------------------------------------------------
#
#----------global-vars----------------------------------------------------------
SFODict={"IND":"1C","MIA":"1D","CLV":"1E","DNV":"1F","SEA":"5C","LAR":"5D","WAS":"5E","SFO":"xx","DAL":"9C","NYG":"9D","CHI":"9E","MIN":"9F"}
MIADict={"IND":"04","MIA":"xx","CLV":"06","DNV":"07"}
defeatedDict={"IND":1,"MIA":2,"CLV":4,"DNV":8,"SEA":16,"LAR":32,"WAS":64,"SFO":128,"DAL":256,"NYG":512,"CHI":1024,"MIN":2048}
SFObaseDict={"IND":"B8F","MIA":"C81","CLV":"C84","DNV":"C89","SEA":"D82","LAR":"E83","WAS":"094","SFO":"xxx","DAL":"D86","NYG":"E87","CHI":"098","MIN":"499"}
masterDict={"SFO":SFODict,"MIA":MIADict}
lastBaseDict={"SFO":SFObaseDict}
#-------------------------------------------------------------------------------
#
#----------main-----------------------------------------------------------------
def main():
  human="SFO"
  defeated=["DNV","WAS","MIN","MIA","DAL","CHI","NYG","IND","SEA","LAR"]
  code=getCode(human,masterDict,defeatedDict,lastBaseDict,defeated).upper()
  print("\n***Compiling password***\n")
  printCode(code,human,defeated)
#-------------------------------------------------------------------------------
#
#----------functions------------------------------------------------------------
#
#-------------------------------------------------------------------------------
# getCode(string,dict,dict,dict,list)
# --human: which human player you are by 3 digit code
# --masterDict: dictionary holding other dictionaries, used for letters AB
# --defeatedDict: dictionary mapping teams to values, used for letters DEF
# --lastBaseDict: dictionary holding other dicionaries, used for letters CGH
# finds the letters piece by piece and puts them into a code string
# RETURNS: code string
#-------------------------------------------------------------------------------
def getCode(human,masterDict,defeatedDict,lastBaseDict,defeated):
  theDict=masterDict[human]
  AB=findAB(theDict,defeated[len(defeated)-1])
  DEF=findDEF(human,defeatedDict,defeated)
  CGH=findCGH(human,lastBaseDict,defeated,defeatedDict)
  return AB+CGH[0]+DEF+CGH[1:]

#-------------------------------------------------------------------------------
# findAB(dict,string)
# --theDict: dictionary mapping who you are and who you beat last to 2-ltr code
# --lastTeamDefeated: 3 letter string representing last team defeated
# looks to dictionary to find numbers AB of password string
# RETURNS: two hex numbers, A and B of password string
#-------------------------------------------------------------------------------
def findAB(theDict,lastTeamDefeated):
  return theDict[lastTeamDefeated]

#-------------------------------------------------------------------------------
# findDEF(string,dict,list)
# --human: 3 letter abbreviation for human player
# --defeatedDict: dictionary mapping each team to their value for defeating
# --defeated: list of teams defeated
# adds up numbers from defeated dict to generate numbers DEF
# RETURNS: three hex numbers, D,E, and F of password string
#-------------------------------------------------------------------------------
def findDEF(human,defeatedDict,defeated):
  num=defeatedDict[human]
  for team in defeated:
    num+=defeatedDict[team]
  DEF=transformMidNum(num)
  return DEF

#-------------------------------------------------------------------------------
# transformMidNum(int)
# --num: number to transform
# this digit must be 3 numbers, if it isn't, this will prepend them on
# if SFO d DEN, generated DEF is only 88. Needs to be 088.
# RETURNS: DEF, guaranteed to be 3 numbers long
#-------------------------------------------------------------------------------
def transformMidNum(num):
  DEF=justHex(num)
  lenDEF=len(DEF)
  for i in range(lenDEF,3):
    DEF="0"+DEF
  return DEF

#-------------------------------------------------------------------------------
# findCGH(string,dict,list,dict)
# --human: 3 letter string representing human
# --baseDict: dict of dicts, mapping each team to their base set dictionary
# --defeated: list of teams defeated
# --defeatedDict: number map for each team defeated
# manipulates CGH from base set to final number. In order of H, C, G.
# note defeated[:-1], don't use last team defeated, but do use self
# RETURNS: CGH
#-------------------------------------------------------------------------------
def findCGH(human,baseDict,defeated,defeatedDict):
  teamDict=baseDict[human]
  lastWin=defeated[len(defeated)-1]
  base=teamDict[lastWin]
  CGH=transformH(human,base,defeated[:-1],defeatedDict)  
  CGH=transformCG(human,CGH,defeated[:-1],defeatedDict)
  return ''.join(CGH)

#-------------------------------------------------------------------------------
# transformH(string,string,list,dict)
# --human: 3 letter string representing human
# --base: 3 letter base from last team defeated and human
# --defeated: list of defeated teams
# --defeatedDict: maps defeated teams to numeric value
# transforms H based on victories over IND, MIA, CLV, DEN
# these teams are represented, in part, by defeated dict vals < 16
# always add human player
# if H rolls over, adds 1 to number C
# G is unmodified by changes to H
# RETURNS: CGH, with H in it's final state (and in hex)
#-------------------------------------------------------------------------------
def transformH(human,base,defeated,defeatedDict):
  H=hexToDecimal(base[2])
  addSum=0
  for team in defeated:
    if defeatedDict[team]<16:
      addSum+=defeatedDict[team]
  if defeatedDict[human] < 16:      
    addSum+=defeatedDict[human]
  temp=H+addSum
  C=hexToDecimal(base[0])
  C+=temp // 16
  C=justHex(C%16)
  H=justHex(temp%16)
  return ''.join((C,base[1],H))

#-------------------------------------------------------------------------------
# transformH(string,string,list,dict)
# --human: 3 letter string representing human
# --base: 3 letter base from last team defeated and human
# --defeated: list of defeated teams
# --defeatedDict: maps defeated teams to numeric value
# takes in H but does not modify it
# transforms C based on victories over SEA,LAR and NFC teams
# these teams are represented in part, by defeated dict values > 16
# always add human player
# if C rolls over, adds 1 to number H
# RETURNS: CGH with all numbers final (and in hex)
#-------------------------------------------------------------------------------
def transformCG(human,CGH,defeated,defeatedDict):
  H=CGH[2]
  addSum=0
  C=hexToDecimal(CGH[0])
  G=hexToDecimal(CGH[1])
  for team in defeated:
    if defeatedDict[team]>=16:
      addSum+=baseDigitMod(defeatedDict[team])
      print("sum = %s after adding %s" % (addSum,team))
  if defeatedDict[human]>=16:
    addSum+=baseDigitMod(defeatedDict[human])
    print("sum = %s after adding %s" % (addSum,human))
  print("C = %s" % C)
  temp=C+addSum
  print("Temp = %s" % temp)
  nums=justHex(temp)
  C=nums[-1]
  #if len(nums >1), that means that C rolled over, roll over gets added to G
  if len(nums)==2:
    G=G+int(nums[0])
  return ''.join((C,justHex(G),H))

#-------------------------------------------------------------------------------
# baseDigitMod(num)
# takes defeated dict and turns it into a 1,2,4, or 8
# Example: Seattle's number is 16, and they get mapped to 1
# --16 = 4, log 2, which is % 0, 2 ^ 0 = 1
# IMPORT: math
# RETURNS: Number 1, 2, 4, or 8, depending on team defeatedDict #
#-------------------------------------------------------------------------------
def baseDigitMod(num):
  logNum=math.log(num,2)%4
  return int(2**logNum)

#-------------------------------------------------------------------------------
# justHex(int)
# --base10Num: number in base 10
# hex numbers are '0x___'
# RETURNS: string representing base10 number in hex, minus 0x
#-------------------------------------------------------------------------------
def justHex(base10Num):
  return str(hex(base10Num)[2:])

#-------------------------------------------------------------------------------
# prependHex(int)
# --hexNum: number in hex
# turns a number back into proper hex format
# RETURNS: string of hex number, with '0x' prepended.
#-------------------------------------------------------------------------------
def prependHex(hexNum):
  return "0x"+str(hexNum)

#-------------------------------------------------------------------------------
# hexToDecimal(int)
# --num: hex number, '0x<num>'
# converts number back to base 10
# RETURNS: base 20 representation of hex number
#-------------------------------------------------------------------------------
def hexToDecimal(num):
  num=prependHex(num)
  return int(num,16)

#-------------------------------------------------------------------------------
# printCode(string,string,list)
# RETURNS: nothing
#-------------------------------------------------------------------------------
def printCode(code,human,defeated):
  print("Playing as %s" % human)
  print("Defeated: ")
  for team in defeated:
    print("\t%s" % team)
  print("Password is %s" % code)

#----------if-name-is-main------------------------------------------------------
if __name__=="__main__":
  main()
