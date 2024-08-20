'''
N = 45
 101101
+     1 padding it so it can start with length 1
 101110
-  1110 = V = value of V.
 100000       we know the first number will always start with 1,
-    10       so we get rid of it.
  11110 = L = length of N. in bits we subtract 1 to make a terminator
 011110 padding it so it match the L length.
N = LV = 01111001110
'''
def elias_gamma_encoder(num): # variable bit integer
	num += 1
	V = num & ((1 << num.bit_length() - 1) - 1)
	num -= V + 2
	L = num
	return (L << num.bit_length()) | V

'''
N = 45
 11110 = L
+ 1110 = V
101100
+    1 to unpadding and get the value back.
101101
'''
def elias_gamma_decoder(encoded_num):
	bit_size = max(1, encoded_num.bit_length() // 2)
	L = encoded_num >> bit_size
	value_mask = int(''.join(['1' for _ in range(bit_size)]), 2)
	V = encoded_num & value_mask
	return L + V + 1

def test_elias_gamma():
	test_pass = True
	for n in range(1, 1_000_000):
		a = elias_gamma_encoder(n)
		b = elias_gamma_decoder(a)
		if a < 0:
			print(f"Error: a is a negative number {a} < 0")
			test_pass = False
		elif b != n:
			print(f"Error: b {b} decode does not match n {n}")
			test_pass = False
	return test_pass

if __name__ == '__main__':
	# num = 2**32-1
	num = 45
	a = elias_gamma_encoder(num)
	print(f"bin(a)[2:] | {bin(a)[2:]}")
	print(f"len(bin(a)[2:]) | {len(bin(a)[2:])}")
	print(f"b | {a}")

	b = elias_gamma_decoder(a)
	print(f"bin(b)[2:] | {bin(b)[2:]}")
	print(f"len(bin(b)[2:]) | {len(bin(b)[2:])}")
	print(f"b | {b}")

	if a < 0:
		print(f"Error: a is a negative number {a} < 0")
	elif num != b:
		print(f"Error: b {b} decode does not match num {num}")

	print('test_elias_gamma() pass =', test_elias_gamma())
