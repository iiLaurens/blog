Title: Scraping media from TTMIK
Slug: scraping-media-from-TTMIK
Date: 2016-05-22 12:44
Tags: Korean, web, scraping, Python
Author: Laurens

My previous post already revealed that I like to study Korean. Mastering the Korean
language is not an easy task so every little bit that helps to make it more
convenient or easier will help study. Having local copies of the study material
provided by the folks at [Talk To Me in Korean](wTalktomeinkorean.com) already goes
a long way.

I have a Python script laying around that did exactly this. It crawls
the pages of TTMIK and collects all PDF files and podcasts of the lessons from level 1 to 9 to a folder. All
the details belonging to the levels are automatically indexed in a `txt` document:

```
1	1	1	Hello, Thank you / 안녕하세요, 감사합니다	TTMIK 001 - Level 1 Lesson 1
2	1	2	Yes, No, What? / 네, 아니요, 네?	TTMIK 002 - Level 1 Lesson 2
3	1	3	Good-bye, See you / 안녕히 가세요, 안녕히 계세요, 안녕	TTMIK 003 - Level 1 Lesson 3
4	1	4	I’m sorry, Excuse me / 죄송합니다, 저기요	TTMIK 004 - Level 1 Lesson 4
5	1	5	It’s me, What is it? / 이에요,예요	TTMIK 005 - Level 1 Lesson 5
6	1	6	What is this?,  This is …. / 이거, 이거 뭐예요?	TTMIK 006 - Level 1 Lesson 6
7	1	7	This, That, It / 이, 그, 저	TTMIK 007 - Level 1 Lesson 7
8	1	8	It’s NOT me / 아니에요	TTMIK 008 - Level 1 Lesson 8
9	1	9	topic,subject marking particles / 은, 는, 이, 가	TTMIK 009 - Level 1 Lesson 9
10	1	10	have, don’t have, there is, there isn’t / 있어요, 없어요	TTMIK 010 - Level 1 Lesson 10
11	1	11	Please give me / 주세요	TTMIK 011 - Level 1 Lesson 11
12	1	12	it’s delicious, it tastes awful, thank you for the food / 맛있어요, 맛없어요, 잘 먹겠습니다, 잘 먹었습니다	TTMIK 012 - Level 1 Lesson 12
13	1	13	I want to … / -고 싶어요	TTMIK 013 - Level 1 Lesson 13
14	1	14	What do you want to do? / 뭐 하고 싶어요?	TTMIK 014 - Level 1 Lesson 14
15	1	15	Sino-Korean Numbers / 일, 이, 삼, 사 ….	TTMIK 015 - Level 1 Lesson 15
16	1	16	Basic Present Tense / -아요, -어요, -여요	TTMIK 016 - Level 1 Lesson 16
17	1	17	Past Tense / -았/었/였어요 (했어요)	TTMIK 017 - Level 1 Lesson 17
18	1	18	Location-marking Particles / 에/에서	TTMIK 018 - Level 1 Lesson 18
19	1	19	When / 언제	TTMIK 019 - Level 1 Lesson 19
20	1	20	Native Korean numbers / 하나, 둘, 셋, 넷 …	TTMIK 020 - Level 1 Lesson 20
21	1	21	Negative Sentences / 안, -지 않다, 안 하다, 하지 않다	TTMIK 021 - Level 1 Lesson 21
22	1	22	verbs / 하다	TTMIK 022 - Level 1 Lesson 22
23	1	23	Who? / 누구?	TTMIK 023 - Level 1 Lesson 23
24	1	24	Why? How? / 왜? 어떻게?	TTMIK 024 - Level 1 Lesson 24
25	1	25	From A To B,  From C Until D / -에서/부터 -까지	TTMIK 025 - Level 1 Lesson 25
26	2	1	Future Tense / -ㄹ/을 거예요, 할 거예요	TTMIK 026 - Level 2 Lesson 1
27	2	2	object marking particles / 을, 를	TTMIK 027 - Level 2 Lesson 2
28	2	3	and, and then, therefore, so / 그리고, 그래서	TTMIK 028 - Level 2 Lesson 3
29	2	4	and, with / 하고, (이)랑	TTMIK 029 - Level 2 Lesson 4
30	2	5	days in a week / 요일	TTMIK 030 - Level 2 Lesson 5
31	2	6	but, however / 그렇지만, 그런데	TTMIK 031 - Level 2 Lesson 6
32	2	7	“to” someone, “from” someone / 한테, 한테서	TTMIK 032 - Level 2 Lesson 7
33	2	8	Telling the time / 한 시, 두 시, 세 시, 네 시 …	TTMIK 033 - Level 2 Lesson 8
34	2	9	Counters / 개, 명	TTMIK 034 - Level 2 Lesson 9
35	2	10	Present Progressive / -고 있어요	TTMIK 035 - Level 2 Lesson 10
36	2	11	Self-introduction / 자기소개	TTMIK 036 - Level 2 Lesson 11
37	2	12	What date is it? / 날짜	TTMIK 037 - Level 2 Lesson 12
38	2	13	too, also / -도 – Part 1	TTMIK 038 - Level 2 Lesson 13
39	2	14	too, also / -도 – Part 2	TTMIK 039 - Level 2 Lesson 14
40	2	15	only / -만	TTMIK 040 - Level 2 Lesson 15
41	2	16	Very, A bit, Really, Not really, Not at all / 조금, 아주, 정말, 전혀, 별로, 진짜	TTMIK 041 - Level 2 Lesson 16
42	2	17	can, cannot / -ㄹ 수 있다/없다	TTMIK 042 - Level 2 Lesson 17
43	2	18	to be good/poor at ~ / 잘 하다/못 하다	TTMIK 043 - Level 2 Lesson 18
44	2	19	Making verbs into nouns / -는 것	TTMIK 044 - Level 2 Lesson 19
45	2	20	have to, should, must / -아/어/여야 되다/하다	TTMIK 045 - Level 2 Lesson 20
46	2	21	more ~ than ~ / ~보다 더	TTMIK 046 - Level 2 Lesson 21
47	2	22	to like / 좋다 vs 좋아하다	TTMIK 047 - Level 2 Lesson 22
48	2	23	if, in case / 만약, -(으)면	TTMIK 048 - Level 2 Lesson 23
49	2	24	still, already / 아직, 벌써	TTMIK 049 - Level 2 Lesson 24
50	2	25	something, someday, someone, somewhere / 누군가, 무언가, 어딘가, 언젠가	TTMIK 050 - Level 2 Lesson 25
51	2	26	imperative / -(으)세요	TTMIK 051 - Level 2 Lesson 26
52	2	27	Do it for me / -아/어/여 주세요	TTMIK 052 - Level 2 Lesson 27
53	2	28	method, way / (으)로	TTMIK 053 - Level 2 Lesson 28
54	2	29	more, all / 더, 다	TTMIK 054 - Level 2 Lesson 29
55	2	30	Don’t do it / -지 마세요	TTMIK 055 - Level 2 Lesson 30
56	3	1	too much or very / 너무	TTMIK 056 - Level 3 Lesson 1
57	3	2	linking verbs with -고 / Verb and Verb / 하고	TTMIK 057 - Level 3 Lesson 2
58	3	3	in front of, behind, on top of, under, next to / 앞에, 옆에, 위에, 밑에, 뒤에	TTMIK 058 - Level 3 Lesson 3
59	3	4	shall we…? + I wonder… / -(으)ㄹ까요?	TTMIK 059 - Level 3 Lesson 4
60	3	5	approximately, about / 쯤, 약, 정도	TTMIK 060 - Level 3 Lesson 5
61	3	6	future tense / -(으)ㄹ 거예요 vs -(으)ㄹ게요	TTMIK 061 - Level 3 Lesson 6
62	3	7	linking verbs / -아/어/여서	TTMIK 062 - Level 3 Lesson 7
63	3	8	to look like, to seem like / – 같아요	TTMIK 063 - Level 3 Lesson 8
64	3	9	to seem like, to look like (used with verbs) / 한 것 같아요	TTMIK 064 - Level 3 Lesson 9
65	3	10	Before -ing / -기 전에	TTMIK 065 - Level 3 Lesson 10
66	3	11	ㅂ irregular / ㅂ 불규칙	TTMIK 066 - Level 3 Lesson 11
67	3	12	But still, nevertheless / 그래도	TTMIK 067 - Level 3 Lesson 12
68	3	13	Making adjectives (Part 2) / descriptive verbs + -ㄴ 명사	TTMIK 068 - Level 3 Lesson 13
69	3	14	 Making adjectives / action verbs + -는/(으)ㄴ/(으)ㄹ + 명사	TTMIK 069 - Level 3 Lesson 14
70	3	15	well then, in that case, if so / 그러면, 그럼	TTMIK 070 - Level 3 Lesson 15
71	3	16	Let’s / -아/어/여요 (청유형)	TTMIK 071 - Level 3 Lesson 16
72	3	17	in order to, for the sake of / 위하다, 위해, 위해서	TTMIK 072 - Level 3 Lesson 17
73	3	18	nothing but, only / 밖에 + 부정형	TTMIK 073 - Level 3 Lesson 18
74	3	19	after -ing / 다음에	TTMIK 074 - Level 3 Lesson 19
75	3	20	even if, even though / -아/어/여도	TTMIK 075 - Level 3 Lesson 20
76	3	21	linking verbs / -는데, 명사 + -인데, 형용사 + -ㄴ데	TTMIK 076 - Level 3 Lesson 21
77	3	22	maybe I might… / -(ㅇ)ㄹ 수도 있어요	TTMIK 077 - Level 3 Lesson 22
78	3	23	Word builder #1 / 학(學)	TTMIK 078 - Level 3 Lesson 23
79	3	24	르 irregular / 르 불규칙	TTMIK 079 - Level 3 Lesson 24
80	3	25	verb ending / -네요	TTMIK 080 - Level 3 Lesson 25
81	3	26	ㄷ irregular / ㄷ 불규칙	TTMIK 081 - Level 3 Lesson 26
82	3	27	Politeness Levels /  반말 and 존댓말	TTMIK 082 - Level 3 Lesson 27
83	3	28	“Let’s” in casual language / 반말, -자 (청유형)	TTMIK 083 - Level 3 Lesson 28
84	3	29	ㅅ irregular / ㅅ 불규칙	TTMIK 084 - Level 3 Lesson 29
85	3	30	Word builder 2 / 실(室)	TTMIK 085 - Level 3 Lesson 30
86	4	1	The more … the more … / -면 -을수록	TTMIK 086 - Level 4 Lesson 1
87	4	2	Do you want to …? / -(으)ㄹ래요?	TTMIK 087 - Level 4 Lesson 2
88	4	3	It can’t be … /-(으)ㄹ 리가 없어요, 할 리가 없어요	TTMIK 088 - Level 4 Lesson 3
89	4	4	verb ending /  -지요/-죠	TTMIK 089 - Level 4 Lesson 4
90	4	5	“당신” and “you” / 당신	TTMIK 090 - Level 4 Lesson 5
91	4	6	Word builder 3 / 동(動)	TTMIK 091 - Level 4 Lesson 6
92	4	7	It’s okay. I’m okay. /  괜찮아요	TTMIK 092 - Level 4 Lesson 7
93	4	8	it is okay to…, you don’t have to… / -아/어/여도 돼요, 해도 돼요	TTMIK 093 - Level 4 Lesson 8
94	4	9	you shouldn’t…, you’re not supposed to… / -(으)면 안 돼요, 하면 안 돼요	TTMIK 094 - Level 4 Lesson 9
95	4	10	among, between / 사이에, 사이에서, 중에, 중에서	TTMIK 095 - Level 4 Lesson 10
96	4	11	anybody, anything, anywhere / 아무나, 아무도, 아무거나, 아무것도	TTMIK 096 - Level 4 Lesson 11
97	4	12	to try doing something / -아/어/여 보다, 해 보다	TTMIK 097 - Level 4 Lesson 12
98	4	13	Word builder 4 / 불(不)	TTMIK 098 - Level 4 Lesson 13
99	4	14	sometimes, often, always, never, seldom / 가끔, 자주, 별로, 맨날, 항상	TTMIK 099 - Level 4 Lesson 14
100	4	15	any / 아무 Part 2	TTMIK 100 - Level 4 Lesson 15
101	4	16	Spacing in Korean / 띄어쓰기	TTMIK 101 - Level 4 Lesson 16
102	4	17	Word Contractions – Part 1 / 주격 조사, 축약형	TTMIK 102 - Level 4 Lesson 17
103	4	18	most, best (superlative) / 최상급, 최고	TTMIK 103 - Level 4 Lesson 18
104	4	19	Less, Not completely / 덜	TTMIK 104 - Level 4 Lesson 19
105	4	20	Sentence Building Drill #1	TTMIK 105 - Level 4 Lesson 20
106	4	21	Spacing Part 2 / 띄어쓰기	TTMIK 106 - Level 4 Lesson 21
107	4	22	Word builder 5 / 장(場)	TTMIK 107 - Level 4 Lesson 22
108	4	23	Word Contractions – Part 2 / 어떻게/어떡해 – 그렇게 하세요/그러세요, 축약형	TTMIK 108 - Level 4 Lesson 23
109	4	24	much more, much less / 훨씬	TTMIK 109 - Level 4 Lesson 24
110	4	25	-(으)ㄹ + noun (future tense noun group) / -(으)ㄹ + 명사, 할 것	TTMIK 110 - Level 4 Lesson 25
111	4	26	-(으)ㄴ + noun (past tense noun group) / -(으)ㄴ + 명사, 한 것	TTMIK 111 - Level 4 Lesson 26
112	4	27	I think … (+ future tense) / -(으)ㄴ/(으)ㄹ/ㄴ 것 같다, 한 것 같다, 할 것 같다	TTMIK 112 - Level 4 Lesson 27
113	4	28	to become + adjective / -아/어/여지다	TTMIK 113 - Level 4 Lesson 28
114	4	29	to gradually/eventually get to do something / -게 되다, 하게 되다	TTMIK 114 - Level 4 Lesson 29
115	4	30	Sentence Building Drill #2	TTMIK 115 - Level 4 Lesson 30
116	5	1	almost did / -(으)ㄹ 뻔 했다, 할 뻔 했다	TTMIK 116 - Level 5 Lesson 1
117	5	2	-시- (honorific) / -시-, 하시다	TTMIK 117 - Level 5 Lesson 2
118	5	3	Good work / 수고	TTMIK 118 - Level 5 Lesson 3
119	5	4	I guess, I assume / -나 보다	TTMIK 119 - Level 5 Lesson 4
120	5	5	I guess, I assume – Part 2 / -(으)ㄴ가 보다	TTMIK 120 - Level 5 Lesson 5
121	5	6	Word builder 6 / 문(文)	TTMIK 121 - Level 5 Lesson 6
122	5	7	as soon as … / -자마자, 하자마자	TTMIK 122 - Level 5 Lesson 7
123	5	8	It is about to …, I am planning to … /  -(으)려고 하다, 하려고 하다	TTMIK 123 - Level 5 Lesson 8
124	5	9	While I was doing …, … and then … / -다가, 하다가	TTMIK 124 - Level 5 Lesson 9
125	5	10	(say) that S + be / -(이)라고 + nouns	TTMIK 125 - Level 5 Lesson 10
126	5	11	Sentence Building Drill #3	TTMIK 126 - Level 5 Lesson 11
127	5	12	Noun + -(이)라는 + Noun / Someone that is called ABC / Someone who says s/he is XYZ	TTMIK 127 - Level 5 Lesson 12
128	5	13	Word Builder lesson 7 / 회 (會)	TTMIK 128 - Level 5 Lesson 13
129	5	14	-(으)니까, -(으)니 / Since, Because, As	TTMIK 129 - Level 5 Lesson 14
130	5	15	At least, Instead, It might not be the best but… / -(이)라도	TTMIK 130 - Level 5 Lesson 15
131	5	16	Narrative Present Tense in Korean / -(ㄴ/는)다,  하다 vs 해요 vs 한다	TTMIK 131 - Level 5 Lesson 16
132	5	17	Quoting someone in Korean / -(ㄴ/는)다는, -(ㄴ/는)다고	TTMIK 132 - Level 5 Lesson 17
133	5	18	Whether or not / -(으)ㄴ/는지	TTMIK 133 - Level 5 Lesson 18
134	5	19	to tell someone to do something /  Verb + -(으)라고 + Verb	TTMIK 134 - Level 5 Lesson 19
135	5	20	Sentence Building Drill #4	TTMIK 135 - Level 5 Lesson 20
136	5	21	Word Contractions Part 3 / 이거를 –> 이걸, 축약형	TTMIK 136 - Level 5 Lesson 21
137	5	22	Word builder 8 / 식 (食)	TTMIK 137 - Level 5 Lesson 22
138	5	23	it seems like … / I assume … / -(으)려나 보다	TTMIK 138 - Level 5 Lesson 23
139	5	24	Not A But B, Don’t do THIS but do THAT / 말고, -지 말고	TTMIK 139 - Level 5 Lesson 24
140	5	25	Compared to, Relatively / -에 비해서 -ㄴ/은/는 편이다 /	TTMIK 140 - Level 5 Lesson 25
141	5	26	Instead of … / 대신에, -는 대신에	TTMIK 141 - Level 5 Lesson 26
142	5	27	You know, Isn’t it, You see…, Come on… / -잖아(요)	TTMIK 142 - Level 5 Lesson 27
143	5	28	 to have no other choice but to … / -(으)ㄹ 수 밖에 없다	TTMIK 143 - Level 5 Lesson 28
144	5	29	they said that they had done …, they said that they would … / -았/었/였다고, -(으)ㄹ 거라고	TTMIK 144 - Level 5 Lesson 29
145	5	30	Sentence Building Drill #5	TTMIK 145 - Level 5 Lesson 30
146	6	1	How about …? / ~ 어때요?	TTMIK 146 - Level 6 Lesson 1
147	6	2	What do you think about …? / 어떻게 생각하세요? / 어떤 것 같아요?	TTMIK 147 - Level 6 Lesson 2
148	6	3	One of the most … / 가장 ~ 중의 하나	TTMIK 148 - Level 6 Lesson 3
149	6	4	Do you mind if I …? / -아/어/여도 돼요?	TTMIK 149 - Level 6 Lesson 4
150	6	5	I’m in the middle of …-ing / -는 중이에요	TTMIK 150 - Level 6 Lesson 5
151	6	6	Word Builder Lesson 9 / -님	TTMIK 151 - Level 6 Lesson 6
152	6	7	One way or the other / 어차피	TTMIK 152 - Level 6 Lesson 7
153	6	8	I’m not sure if … / -(으/느)ㄴ지 잘 모르겠어요.	TTMIK 153 - Level 6 Lesson 8
154	6	9	While you are at it / -(으)ㄴ/는 김에 /	TTMIK 154 - Level 6 Lesson 9
155	6	10	Sentence Building Drill 6	TTMIK 155 - Level 6 Lesson 10
156	6	11	I mean… / 그러니까, 제 말 뜻은, -라고요, 말이에요	TTMIK 156 - Level 6 Lesson 11
157	6	12	What do you mean? What does that mean? / 무슨 말이에요?	TTMIK 157 - Level 6 Lesson 12
158	6	13	Word Builder 10	TTMIK 158 - Level 6 Lesson 13
159	6	14	“/ (slash)” or “and” /  -(으)ㄹ 겸	TTMIK 159 - Level 6 Lesson 14
160	6	15	the thing that is called, what they call … /  -(이)라는 것	TTMIK 160 - Level 6 Lesson 15
161	6	16	-겠- (suffix)	TTMIK 161 - Level 6 Lesson 16
162	6	17	because, since, let me tell you… / -거든(요)	TTMIK 162 - Level 6 Lesson 17
163	6	18	– Or / -거나, -(이)나, 아니면	TTMIK 163 - Level 6 Lesson 18
164	6	19	to improve, to change, to increase / -아/어/여지다 Part 2	TTMIK 164 - Level 6 Lesson 19
165	6	20	Sentence Building Drill 7	TTMIK 165 - Level 6 Lesson 20
166	6	21	Passive Voice in Korean – Part 1	TTMIK 166 - Level 6 Lesson 21
167	6	22	Word Builder 11 / 무	TTMIK 167 - Level 6 Lesson 22
168	6	23	Passive Voice – Part 2	TTMIK 168 - Level 6 Lesson 23
169	6	24	I DID do it, I DO like it / -기는 하다	TTMIK 169 - Level 6 Lesson 24
170	6	25	Easy/difficult to + V / -기 쉽다/어렵다	TTMIK 170 - Level 6 Lesson 25
171	6	26	I thought I would …, I didn’t think you would … / -(으)ㄴ/ㄹ 줄 알다	TTMIK 171 - Level 6 Lesson 26
172	6	27	can, to be able to, to know how to / -(으)ㄹ 수 있다, -(으)ㄹ 줄 알다	TTMIK 172 - Level 6 Lesson 27
173	6	28	it depends on … / -에 따라 달라요	TTMIK 173 - Level 6 Lesson 28
174	6	29	sometimes I do this, sometimes I do that / 어떨 때는 -고, 어떨 때는 -아/어/여요	TTMIK 174 - Level 6 Lesson 29
175	6	30	Sentence Building Drill 8	TTMIK 175 - Level 6 Lesson 30
176	7	1	I see that …, I just realized that … / -(는)구나 / -(는)군요	TTMIK 176 - Level 7 Lesson 1
177	7	2	to pretend to + V / -(으/느)ㄴ 척/체 하다	TTMIK 177 - Level 7 Lesson 2
178	7	3	to be doable/understandable/bearable / -(으)ㄹ 만하다	TTMIK 178 - Level 7 Lesson 3
179	7	4	like + N / -같이, -처럼	TTMIK 179 - Level 7 Lesson 4
180	7	5	as much as / -((으)ㄹ) 만큼	TTMIK 180 - Level 7 Lesson 5
181	7	6	Word Builder 12 / 원 (院)	TTMIK 181 - Level 7 Lesson 6
182	7	7	even if …, there is no use / -아/어/여 봤자	TTMIK 182 - Level 7 Lesson 7
183	7	8	-길래	TTMIK 183 - Level 7 Lesson 8
184	7	9	-느라고	TTMIK 184 - Level 7 Lesson 9
185	7	10	Sentence Building Drill 9	TTMIK 185 - Level 7 Lesson 10
186	7	11	Making Things Happen (Causative)	TTMIK 186 - Level 7 Lesson 11
187	7	12	-더라(고요)	TTMIK 187 - Level 7 Lesson 12
188	7	13	Word Builder 13 / 기 (機)	TTMIK 188 - Level 7 Lesson 13
189	7	14	No matter how… / 아무리 -아/어/여도	TTMIK 189 - Level 7 Lesson 14
190	7	15	What was it again? / 뭐더라?, 뭐였죠?	TTMIK 190 - Level 7 Lesson 15
191	7	16	I said … / -다니까(요), -라니까(요)	TTMIK 191 - Level 7 Lesson 16
192	7	17	They say …/-(느)ㄴ대요/-(이)래요	TTMIK 192 - Level 7 Lesson 17
193	7	18	They say … / -(느)ㄴ다던데요/-(이)라던데요	TTMIK 193 - Level 7 Lesson 18
194	7	19	Making reported questions / -냐고	TTMIK 194 - Level 7 Lesson 19
195	7	20	Sentence Building Drill 10	TTMIK 195 - Level 7 Lesson 20
196	7	21	Didn’t you hear him say … / -(ㄴ/는)다잖아요/-라잖아요	TTMIK 196 - Level 7 Lesson 21
197	7	22	Word Builder 14 / 정 (定)	TTMIK 197 - Level 7 Lesson 22
198	7	23	no matter whether you do it or not / -(으)나마나	TTMIK 198 - Level 7 Lesson 23
199	7	24	Passive Voice + -어 있다 / To have been put into a certain state	TTMIK 199 - Level 7 Lesson 24
200	7	25	to be bound to + V / -게 되어 있다	TTMIK 200 - Level 7 Lesson 25
201	7	26	on top of …, in addition to … / -(으/느)ㄴ 데다가	TTMIK 201 - Level 7 Lesson 26
202	7	27	As long as / -(느)ㄴ 한, -기만 하면	TTMIK 202 - Level 7 Lesson 27
203	7	28	the thing that is called + Verb / -(ㄴ/는)다는 것	TTMIK 203 - Level 7 Lesson 28
204	7	29	so that …, to the point where … / -도록	TTMIK 204 - Level 7 Lesson 29
205	7	30	Sentence Building Drill 11	TTMIK 205 - Level 7 Lesson 30
206	8	1	Advanced Idiomatic Expressions / 눈 (eye) – Part 1/2	TTMIK 206 - Level 8 Lesson 1
207	8	2	Advanced Idiomatic Expressions / 눈 (eye) – Part 2/2	TTMIK 207 - Level 8 Lesson 2
208	8	3	right after + V-ing / -기가 무섭게, -기가 바쁘게	TTMIK 208 - Level 8 Lesson 3
209	8	4	N + that (someone) used to + V / -던	TTMIK 209 - Level 8 Lesson 4
210	8	5	Advanced Situational Expressions: Refusing in Korean	TTMIK 210 - Level 8 Lesson 5
211	8	6	it means … / -(ㄴ/는)다는 뜻이에요	TTMIK 211 - Level 8 Lesson 6
212	8	7	Word Builder 15 / 점 (點)	TTMIK 212 - Level 8 Lesson 7
213	8	8	I hope …, I wish … / -(으)면 좋겠어요	TTMIK 213 - Level 8 Lesson 8
214	8	9	Past Tense (Various Types) / 과거시제 총정리	TTMIK 214 - Level 8 Lesson 9
215	8	10	Advanced Idiomatic Expressions – 귀 (ear)	TTMIK 215 - Level 8 Lesson 10
216	8	11	Sentence Building Drill 12	TTMIK 216 - Level 8 Lesson 11
217	8	12	Present Tense (Various Types) / 현재시제 총정리	TTMIK 217 - Level 8 Lesson 12
218	8	13	Word Builder 16 / 주 (主)	TTMIK 218 - Level 8 Lesson 13
219	8	14	Advanced Situational Expressions: Agreeing	TTMIK 219 - Level 8 Lesson 14
220	8	15	Future Tense (Various Types) / 미래시제 총정리	TTMIK 220 - Level 8 Lesson 15
221	8	16	Advanced Idiomatic Expressions – 가슴 (chest, heart, breast)	TTMIK 221 - Level 8 Lesson 16
222	8	17	If only it’s not … / -만 아니면	TTMIK 222 - Level 8 Lesson 17
223	8	18	in the same way that …, just like someone did … / -(으)ㄴ 대로	TTMIK 223 - Level 8 Lesson 18
224	8	19	even if I would have to, even if that means I have to / -는 한이 있더라도	TTMIK 224 - Level 8 Lesson 19
225	8	20	Sentence Building Drill 13	TTMIK 225 - Level 8 Lesson 20
226	8	21	Advanced Idiomatic Expressions – 머리 (head, hair)	TTMIK 226 - Level 8 Lesson 21
227	8	22	Word Builder 17 / 상 (上)	TTMIK 227 - Level 8 Lesson 22
228	8	23	Advanced Situational Expressions: Making Suggestions in Korean	TTMIK 228 - Level 8 Lesson 23
229	8	24	it is just that …, I only … / -(으)ㄹ 따름이다	TTMIK 229 - Level 8 Lesson 24
230	8	25	Advanced Situational Expressions: Defending in Korean	TTMIK 230 - Level 8 Lesson 25
231	8	26	Advanced Idiomatic Expressions – 몸 (body)	TTMIK 231 - Level 8 Lesson 26
232	8	27	Advanced Situational Expressions: Complimenting in Korean	TTMIK 232 - Level 8 Lesson 27
233	8	28	despite, in spite of / -에도 불구하고	TTMIK 233 - Level 8 Lesson 28
234	8	29	Advanced Situational Expressions: When You Feel Happy	TTMIK 234 - Level 8 Lesson 29
235	8	30	Sentence Building Drill 14	TTMIK 235 - Level 8 Lesson 30
236	9	1	Advanced Idiomatic Expressions / 손 (Hand)	TTMIK 236 - Level 9 Lesson 1
237	9	2	-아/어/여 버리다	TTMIK 237 - Level 9 Lesson 2
238	9	3	Advanced Situational Expressions: When You Are Unhappy	TTMIK 238 - Level 9 Lesson 3
239	9	4	-고 말다	TTMIK 239 - Level 9 Lesson 4
240	9	5	Advanced Situational Expressions: When you are worried	TTMIK 240 - Level 9 Lesson 5
241	9	6	Advanced Idiomatic Expressions – 발 (foot)	TTMIK 241 - Level 9 Lesson 6
242	9	7	Word Builder 18 / 비 (非)	TTMIK 242 - Level 9 Lesson 7
243	9	8	Advanced Situational Expressions: Asking a favor	TTMIK 243 - Level 9 Lesson 8
244	9	9	-(으)ㅁ	TTMIK 244 - Level 9 Lesson 9
245	9	10	Sentence Building Drill 15	TTMIK 245 - Level 9 Lesson 10
246	9	11	Advanced Idiomatic Expressions – 마음 (mind, heart)	TTMIK 246 - Level 9 Lesson 11
247	9	12	-아/어/여 보이다	TTMIK 247 - Level 9 Lesson 12
248	9	13	Word Builder 19 / 신 (新)	TTMIK 248 - Level 9 Lesson 13
249	9	14	Advanced Situational Expressions: 후회할 때	TTMIK 249 - Level 9 Lesson 14
250	9	15	Advanced Idiomatic Expressions – 기분 (feeling)	TTMIK 250 - Level 9 Lesson 15
251	9	16	-(으)ㄹ 테니(까)	TTMIK 251 - Level 9 Lesson 16
252	9	17	-(으/느)ㄴ 이상	TTMIK 252 - Level 9 Lesson 17
253	9	18	-(으)ㄹ까 보다	TTMIK 253 - Level 9 Lesson 18
254	9	19	Advanced Situational Expressions: 오랜만에 만났을 때	TTMIK 254 - Level 9 Lesson 19
255	9	20	Sentence Building Drill 16	TTMIK 255 - Level 9 Lesson 20
256	9	21	Advanced Idiomatic Expressions – 생각 (thought, idea)	TTMIK 256 - Level 9 Lesson 21
257	9	22	Word builder 20 / 시 (示, 視)	TTMIK 257 - Level 9 Lesson 22
258	9	23	-(으)면서	TTMIK 258 - Level 9 Lesson 23
259	9	24	-(ㄴ/는)다면서(요), -(이)라면서(요)	TTMIK 259 - Level 9 Lesson 24
260	9	25	Advanced Situational Expressions: 길을 물어볼 때	TTMIK 260 - Level 9 Lesson 25
261	9	26	Advanced Idiomatic Expressions – 시간 (time)	TTMIK 261 - Level 9 Lesson 26
262	9	27	-더니	TTMIK 262 - Level 9 Lesson 27
263	9	28	-(으)ㄹ 바에	TTMIK 263 - Level 9 Lesson 28
264	9	29	Advanced Situational Expressions: 차가 막힐 때	TTMIK 264 - Level 9 Lesson 29
265	9	30	Sentence Building Drill 17	TTMIK 265 - Level 9 Lesson 30
```

You might wonder why this is so helpful to me. But that's something for another post.

### Python code
Simply save the script below to a file and run it with python.
```Python
import os
import requests
from bs4 import BeautifulSoup
import codecs


def get_lesson_info(lesson, file_nr, filename):
    # Find the seperator in the title first, as TTMIK is not consistent with it
    for title in lesson.find("h1", class_="entry-title"):
        string = title.string
        splitter = ''
        for i in string:
            if i == '/' or i == 'â€“':
                splitter = ' ' + i + ' '
                break
    # Split title into subcomponents
    strings = string.split(splitter, 1)

    lvl_lssn = strings[0].replace('TTMIK ', '').split(' ')

    # collect data in the list.
    # list = [nr, lvl, lssn, ...]
    strings = [file_nr, lvl_lssn[1], lvl_lssn[-1]] + strings[1:]

    strings = strings + [filename]
    #print(strings)
    with codecs.open("./download/lesson_list.txt", "a", "utf-8") as my_file:  # better not shadow Python's built-in file
        my_file.write('\t'.join([str(i) for i in strings]) + '\r\n')

def get_lesson(lesson, filename):
    for download in lesson.findAll("div", class_="download")[1:3]:
        url = download.a["href"]
        if 'pdf' in url:
            filetype = 'pdf'
        elif 'mp3' in url:
            filetype = 'mp3'

        with open('download/' + filename + '.' + filetype, 'xb') as out_file:
            file = requests.get(url).content
            out_file.write(file)
        del file
        print('>> Succesfully saved ' + filename + '.' + filetype)

def get_level(lvl_nr,file_nr):
    if not os.path.exists("download"):
        os.makedirs("download")
    lssn_nr = 1
    # login
    with requests.Session() as s:
        # get HTML
        url_prefix = 'http://www.talktomeinkorean.com/category/lessons/level-'
        rc = s.get(url_prefix + str(lvl_nr))
        while rc:
            # parse it
            pool = BeautifulSoup(rc.content)
            for lesson in pool.findAll("article", class_="category-lessons"):
                if 'lesson' not in lesson.header.a.contents[0].lower():
                    print('jump')
                    continue
                filename = 'TTMIK {:03d} - Level {} Lesson {}'.format(file_nr, lvl_nr, lssn_nr)
                print('\n Attempting to grab ' + filename)
                get_lesson_info(lesson, file_nr, filename)
                get_lesson(lesson, filename)
                lssn_nr += 1
                file_nr += 1

            if pool.find('a', class_='next'):
                rc = s.get(pool.find('a', class_='next')['href'])
            else:
                rc = False
    return file_nr

def get_levels():
    file_nr = 1
    for i in range(1,10):
        file_nr = get_level(i,file_nr)

if __name__ == '__main__':
    get_levels()

```
