Written By Ken Schroeder
E-mail: schroeder.w.ken@gmail.com
Version 1.0
January 20, 2020
TecmoBowl Password Generator

Team Abbreviations:
IND: Indianapolis
MIA: Miami
CLV: Cleveland
DNV: Denver
SEA: Seattle
LAR: Los Angeles
WAS: Washington
SFO: San Francisco
DAL: Dallas
NYG: New York
CHI: Chicago
MIN: Minnesota

Known Passwords:
SFO - DNV														 			  1F408899	
SFO - DNV,WAS	  												    5E80C89C			
SFO - DNV,WAS,MIN 											 	  9F18C8A1		
SFO - DNV,WAS,MIN,MIA 										  1D08CAA9	
SFO - DNV,WAS,MIN,MIA,DAL 								  9C29CAA0
SFO - DNV,WAS,MIN,MIA,DAL,CHI							  9E6DCAA2
SFO - DNV,WAS,MIN,MIA,DAL,CHI,NYG					  9D8FCAA1
SFO - DNV,WAS,MIN,MIA,DAL,CHI,NYG,IND		    1C7FCBA9
SFO - all but LAR, Cleveland                5C8FDBAD
SFO - all but Cleveland                     5DAFFBAE

Algorithm with example:
Password variables are !@#$%^&*
Pretend we've defeated DNV, WAS, MIN, MIA as SFO
Step 1: AB
	First, use the AB table and the most recent team to determine !@
	In the top row, find your team (SFO) and go down until you find your most recent victory (MIA) in the columns. In this case, that is 1D. This is the value of !@.

After step 1, your password is 1D#$%^&*

Step 2: DEF
	Go to the defeated table. Add up every team you've defeated (including the most recent team and yourself) into a 3 digit, hexadecimal number. In this example that would be 8CA (8 for Minnesota, C = 12 for WAS + SFO, A=10 for DEN + MIA

After step 2 your password is 1D#8CA&*
	

Step 3: CGH
	Go to the CGH table. Find your team in the top row and go down until you find the 3 digit number representing the team you  most recently defeated.

	In our example, this is MIA and the base digits are C81.

Step 3A: Modify H	
	To modify H, look at the defeated table. Add up the values for all the teams in the first group (IND, MIA, CLE, DEN) UNLESS that team is the most recent team you defeated. Then add in your team, if applicable. In this example, that team is Miami so don't include them. We also don't add in SFO because they are part of group 2.

	Add this sum to H. In this case, that value is 9 which will be our final H value.

	If, for example, the base digits were C8C and you defeated Denver, that would make H 20. What we would do in this case is roll it over, modulo 16 to 4, and we would add 1 to the value of C. More on that below.

After 3A, our password is ID#8CA&9, temp # = C, temp * = 8

Step 3B:
	Look at the defeated values and add up the defeated values for all teams outside of the original 4 group, plus your team. Just take the non-zero digit (e.g. 1 for Dallas, not 100 or 256, etc). But do not include your most recently defeated team. In this example we include SFO because they are in group 2 and include all defeated teams from the groups since our most recently defeated team (MIA) is in group 1.

	WAS + SFO + MIN = 20

	Add 20 to # to get 32.

	32 // 16 = 2, so we add 2 to & to get our final & value of A
	32 % 16 = 0, which is our final value of #.

FINAL PASSWORD: 1D08CAA9


AB Table
				IND - MIA - CLV - DNV - SEA - LAR - WAS - SFO - DAL - NYG - CHI - MIN		
  IND   xx    04    08    0C    10    14    18    1C    20    24    28    2C  
  MIA   01    xx    09    0D    11    15    19    1D    21    25    29    2D
  CLV   02    06    xx    0E    12    16    1A    1E    22    26    2A    2E
  DNV   03    07    0B    xx    13    17    1B    1F    23    27    2B    2F
  SEA   40    44    48    4C    xx    54    58    5C    60    64    68    6C
  LAR   41    45    49    4D    51    xx    59    5D    61    65    69    6D
  WAS   42    46    4A    4E    52    56    xx    5E    62    66    6A    6E
  SFO   43    47    4B    4F    53    57    5B    xx    63    67    6B    6F
  DAL   80    84    88    8C    90    94    98    9C    xx    A4    A8    AC
  NYG   81    85    89    8D    91    95    99    9D    A1    xx    A9    AD
  CHI   82    86    8A    8E    92    96    9A    9E    A2    A6    xx    AE
  MIN   83    87    8B    8F    93    97    9B    9F    A3    A7    AB    xx


Defeated table
  IND	001
  MIA	002
  CLE	004
  DEN	008
  
  SEA	010
  LAR	020
  WAS	040
  SFO	080
  
  DAL	100
  NYG	200
  CHI	400
  MIN	800

Base Digits Table
		   IND - MIA - CLV - DNV - SEA - LAR - WAS - SFO - DAL - NYG - CHI - MIN - 
	IND  xxx   B89   B8A   B8B   B8C   B8D   B8E   B8F   C80   C81   C82   C83   
	MIA  B8A   xxx   B8C   B8D   B8E   B8F   C80   C81   C82   C83   C84   C85   
  CLV  B8D   B8E   xxx   C80   C81   C82   C83   C84   C85   C86   C87   C88   
  DNV  C82   C83   C84   xxx   C86   C87   C88   C89   C8A   C8B   C8C   C8D   
  SEA  C8B   C8C   C8D   C8E   xxx   D80   D81   D82   D83   D84   D85   D86   
  LAR  D8C   D8D   D8E   D8F   E80   xxx   E82   E83   E84   E85   E86   E87   
  WAS  F8D   F8E   F8F   090   091   092   xxx   094   095   096   097   098   
  SFO  39E   39F   490   491   492   493   494   xxx   496   497   498   499   
  DAL  C8F   D80   D81   D82   D83   D84   D85   D86   xxx   D88   D89   D8A   
  NYG  E80   E81   E82   E83   E84   E85   E86   E87   E88   xxx   E8A   E8B   
  CHI  091   092   093   094   095   096   097   098   099   09A   xxx   09C   
  MIN  492   493   494   495   496   497   498   499   49A   49B   49C   xxx   



