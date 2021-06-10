def string_to_int(string):
    base = 4
    x = ""
    for i in string:
        c = str(ord(i))
        while len(c) != base:
            c = '0' + c #0000
        x+= c
    return int(x)

def int_to_base64(a: int):
    r = ""
    dig ="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-+"
    while a != 0:
        r+=dig[a % 64]
        a //= 64
    r = r[::-1]
    return r

def get_id(ch):
    if ch == '-':
        return 62
    if ch == '+':
        return 63
    if ch <= '9':
        return int(ch)
    if ch <= 'Z':
        return ord(ch) - ord('A') + 10
    return ord(ch) - ord('a') + 36

def base64_to_int(r):
	a = 0;
	for i in r:
		a*= 64
		a+= get_id(i)
	return a


