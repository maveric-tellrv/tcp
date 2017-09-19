from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from heapq import nlargest,nsmallest
from collections import defaultdict,Counter
import sys,os,xlwt


module = __import__(sys.argv[2].replace('.py', ''))

sentence = sent_tokenize(module.tc)
#print (sentence)
ranking = defaultdict(int)

wb = xlwt.Workbook()


def summarize(tc,n):
	sents = sent_tokenize(tc)
	assert n <= len(sents)
	word_sent= word_tokenize(tc.lower())

	_stopwords = set(stopwords.words('english') + list(punctuation))
	# _stopwords

	word_sent = [word for word in word_sent if word not in _stopwords]
	#word_sent
	
	freq = FreqDist(word_sent)
	#freq

	
	ranking = defaultdict(int)
	ranking_with_tc = defaultdict(int)

	for i,sent in enumerate(sentence):
    		for w in word_tokenize(sent.lower()):
        		if w in freq:
                		ranking[i] += freq[w]
        
        print ranking

	ranking_with_tc = Counter(ranking) +  Counter(module.tc_rank)
 




	#sent_idx1 = nsmallest(n,ranking,key=ranking.get)
	sent_idx2 = nlargest(n,ranking,key=ranking.get)
	#sent_idx

	#[sentence[j] for j in sorted(sent_idx)]
	#for j in sent_idx1:
    	#	print j," -> "+sentence[j]
	
	print ("/nLarget_Priority/n")	
	for j in sent_idx2:
    		print "TC",j," -> "+sentence[j]
    		#print sentence[j]
	
	print("---------#####--Priority Considering Feature and Bug Fixes---######------------")

	ranking_with_tc = Counter(ranking) +  Counter(module.tc_rank)
	sent_idx_rank = nlargest(n,ranking,key=ranking_with_tc.get)
	#for j in sent_idx_rank:
        #        print "TC",j," -> "+sentence[j]



# Adding the workbook sheet for Priortized test considering Bugs and Feature
	data = []
	x = []
	#wb = xlwt.Workbook()
	ws = wb.add_sheet("Priority_Test")


	for j in sent_idx_rank:
                print "TC",j," -> "+sentence[j]
		x = ("TC"+str(j),sentence[j])
		data.append(x)
#	print data
	ws.write(0,0,"Test case No")
        ws.write(0,1,"Test case title")

	for i, row in enumerate(data):
    		for j, col in enumerate(row):
        		ws.write(i+1, j, col)
	#ws.col(0).width = 256 * max([len(row[0]) for row in data])
        #wb.save("myworkbook.xls")


#Adding the ranking values
	excel_func("ranking","ranking.xlx",ranking_with_tc,"Tc_case","Rank_score")

# Adding the workbook sheet for Priortized test 

	data1 = []
        x1 = []
        #wb = xlwt.Workbook()
        ws = wb.add_sheet("Priority_Test_wo")


        for j in sent_idx2:
                print "TC",j," -> "+sentence[j]
                x1 = ("TC"+str(j),sentence[j])
                data1.append(x1)
        #print data

        for i, row in enumerate(data1):
                for j, col in enumerate(row):
                        ws.write(i, j, col)
 
	wb.save("myworkbook.xls")

	#excel_func("ranking","ranking.xlx",ranking)

def excel_func(sheet_name,wb_name,dict_val,col1_name,col2_name):
        ws = wb.add_sheet(sheet_name)
	ws.write(0,0,col1_name)
        ws.write(0,1,col2_name)

        for i,row in enumerate(dict_val.items()):
                for j,col in enumerate(row):
                        ws.write(i+1,j,col)

if __name__ == "__main__":
	n1 = sys.argv[1]
	summarize(module.tc,int(n1))
	os.system('libreoffice myworkbook.xls &')
