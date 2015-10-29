#
#
#
#

bLine=[]
k=""

firstNote = [1,8,15]


def inputBassLine(bassLine):
    if (goodBassLine(bassLine)):
        bLine=bassLine
    else:
        print "Bad bass line, try again"

def goodBassLine(bassLine):
	if bassLine[0] not in firstNote:
		return False


	if len(bassLine)!= 8:
		return False

	for index in range(len(baseLine)-1):
		if math.abs(bLine[index] - bLine[index+1]) >= 7 :
			return False

	if bassLine[7] not in firstNote:
		return False

	return True

    
    
    
    
