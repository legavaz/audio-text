


# def convert_to_preferred_format(secund): 
# 	m_sec = secund % (24 * 3600) 
#     m_hour = secund / 3600
    
#     sec %= 3600 
#     min = sec // 60 
#     sec %= 60 
#     # return "%02d:%02d:%02d" % (hour, min, sec) 
    
# n = 10000     


sec = 125

sec = sec % (24 * 3600)
hour = sec // 3600
sec %=3600
min = sec // 60
sec %=60

a = "%02d:%02d" % (min,sec)


print("Time in preferred format :-",a )
