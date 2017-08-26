from itertools import accumulate
from random import randint
from sys import argv

#Program
flag = argv[1]

program, input_list = None, None

if flag is 'i':
	input_list = ''.join(open(argv[3]))
elif flag is 'w':
	input_list = ' '.join(argv[3:])

program = ''.join(open(argv[2])).strip('\n').strip(' ')

#Setup
tape = [0]*30000
pointer = 0
output = ''
storage = None

#Debug
debugging = False
def debug(*arg):
	if debugging: print(list(arg))

#Core
bracket_index = lambda s,i,opn,cls: next((i for i,x in enumerate(accumulate({opn: 1, cls: -1}.get(c,0) for c in s[i:]), i) if not x), None)

def take_input():
	global input_list
	if len(input_list):
		tape[pointer]=ord(input_list[0])
		if len(input_list) == 1 : input_list = ''
		else: input_list = input_list[1:]
	else:
		tape[pointer]=0
def increment():tape[pointer]=randint(tape[pointer]+1,255) if tape[pointer]!=255 else 0
def decrement():tape[pointer]=randint(0,tape[pointer]-1) if tape[pointer]!=0 else 255
def moveRight():global pointer;pointer=(pointer+1)%len(tape)
def moveLeft():global pointer;pointer=(pointer-1)%len(tape)
def echo():global output;output+=chr(tape[pointer])
def copy():global storage;storage=tape[pointer]
def paste():tape[pointer]=(tape[pointer]+storage)%256
def generate():tape[pointer]=randint(0,255)

function = {
	'>': moveRight,
	'<': moveLeft,
	'|': generate,
	'+': increment,
	'-': decrement,
	'.': echo,
	',': take_input,
	'?': copy,
	'!': paste
}

def execute(code,next_parse=0):

	for i, char in enumerate(code):
		if not next_parse:
			if char in function:function[char]()

			elif char in '[({': # Other functions
				if char is '[': # While loop
					next_parse=bracket_index(code,i,'[',']')
					while tape[pointer]:execute(code[i+1:next_parse])

				elif char is '(': # If
					next_parse=bracket_index(code,i,'(',')')
					if tape[pointer]:execute(code[i+1:next_parse])

				elif char is '{': # If not
					next_parse=bracket_index(code,i,'{','}')
					if not tape[pointer]:execute(code[i+1:next_parse])

		elif i+1 is next_parse or i>=next_parse: next_parse = 0

		#Debug
		debug(char, pointer, tape[pointer], not next_parse, next_parse)

if __name__ == '__main__':
	execute(program)
	print(output)
	#Debug
	debug(tape[pointer])
