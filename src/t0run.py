import subprocess
import select
import os

class Implementation(object):

	def __init__(self):
		self._sub = subprocess.Popen(
			args = ['python', 't0dos.py'],
			stdin = subprocess.PIPE,
			stdout = subprocess.PIPE,
			)

	def read(self):
		buffer = ''
		while not buffer.endswith('>>'):
			ready = select.select([self._sub.stdout],
				[],
				[self._sub.stdout])

			buffer += os.read(self._sub.stdout.fileno(), 1024)

			if buffer.endswith('***MORE***'):
				print '(more)'
				buffer = buffer[:-10]
				self._sub.stdin.write('\n')

		return buffer

	def write(self, command):
		self._sub.stdin.write(command + '\n')

	def close(self):
		print 'Terminating process', self._sub.pid, 'here'
		self._sub.terminate()
		print 'Waiting...'
		self._sub.wait()

class Script(object):
	def __init__(self, implementation):
		print 'script init.'
		self._implementation = implementation

		# we just throw this away, because it's
		# init information which varies by implementation
		# and isn't useful except for debugging

		self._implementation.read()

	def do(self,
		command,
		expect=None):
		
		print '====', command

		self._implementation.write(command)
		result = self._implementation.read()

		print result

		if expect is not None and not expect in result:
			self._implementation.close()
			raise Exception('"%s" was not found in:\n%s' % (expect, result))

		return result

class Playthrough(Script):
	def run(self):
		self.do('inventory', expect = 'in your possession')
		self.do('x slip', expect='walking papers')
		self.do('read slip', expect='too near completion')
		self.do('x compass', expect='cardinal directions')
		self.do('x me', expect='fade into the woodwork')
		self.do('x journal page', expect='cryptic')
		self.do('x fatigues', expect='commodious')
		self.do('x fob pocket', expect='just the right')
		self.do('x thigh pocket', expect='mind of its own')

		# Field of Poppies

		self.do('nw', expect='Field of Poppies')
		self.do('x poppy', expect='dry husk')
		self.do('get seed', expect='bursts')

		# Field of Stone

		self.do('s', expect='Field of Stone')
		birdpoo = ''
		birdpoo += self.do('leave no stone unturned', expect='prehistoric')
		birdpoo += self.do('get claw', expect='Taken')
		birdpoo += self.do('x tern', expect='tirelessly')

		while 'taking aim' not in birdpoo:
			birdpoo += self.do('wait')

		self.do('stone terns', expect='stoned')
		self.do('get tern', expect='turn to stone')
		self.do('get feather', expect='Taken')

		# off to the Coldhouse

		self.do('se', expect='Desolate Field')
		self.do('s', expect='Back of Museum')
		self.do('e', expect='Greenhouse')
		self.do('ne', expect='Coldhouse')

		# Coldhouse

		self.do('pull lever', expect='arctic')
		self.do('get token', expect='Taken')
		self.do('get lever', expect='Taken')

		self.do('sw', expect='Greenhouse')
		self.do('e', expect='Shed')

		# Shed

		self.do('x shelf', expect='splintery')
		self.do('get extractor', expect='Taken')
		self.do('get fixer-upper', expect='Taken')

		self.do('w', expect='Greenhouse')
		self.do('open door', expect='Opened')
		self.do('n', expect='Caretaker\'s Cottage')

		# Cottage

		self.do('get bell', expect='Taken')

		self.do('e', expect='Pantry')

		# Pantry

		self.do('get jar', expect='Taken')

		self.do('w', expect='Caretaker\'s Cottage')
		self.do('s', expect='Greenhouse')
		self.do('se', expect='Fountain Court')
		self.do('s', expect='Topiary')
		self.do('e', expect='Topiary')

		# Topiary

		topiary_path = 'EESSENNNESWSESSWWWWNNESWSEEEEN'

		for move in topiary_path:
			result = self.do(move, 'to the Northwest')

			for line in result.split('\n'):
				words = line.split()

				if len(words)<4:
					continue

				if words[3]!='to' and words[4]!='the':
					continue

				monster = words[1]

				for (affix, tool) in ( ('latch', 'extractor'),
					('key', 'fixer-upper') ):

					if affix in monster:
						self.do('pull '+monster+' with '+tool,
							expect='which now reads')

		self.do('e', expect='Amazing Space')

		# Amazing Space

		self.do('attach fixer-upper to extractor', expect='lightning')
		self.do('get latchkey', expect='Taken')
		self.do('get orange', expect='Taken')

		self.do('e', expect='Platform Over River')
		self.do('ne', expect='Suspension Bridge')
		self.do('snap suspenders', expect='retort')
		self.do('ne', expect='Across the River')
		self.do('e', expect='Junkyard')

		# Junkyard

		self.do('call rag man Anagram', expect='proper name')
		self.do('ask Anagram about violets', expect='wallflower')
		self.do('dig in dump with claw', expect='debugged')
		self.do('get ring', expect='swoops')
		self.do('get code', expect='Taken')
		self.do('get flag', expect='Taken')
		self.do('give code to anagram', expect='wire-frame')

		self.do('w', expect='Across the River')
		self.do('sw', expect='Suspension Bridge')

		self.do('snap suspenders', expect='retort')
		self.do('tie loop to stanchion', expect='infinite')
		self.do('snap suspenders', expect='retort')
		self.do('d', expect='On the Rocks')

		# On the Rocks

		self.do('get coaster', expect='Taken')

		self.do('u', expect='Suspension Bridge')
		self.do('snap suspenders', expect='retort')
		self.do('sw', expect='Platform Over River')
		self.do('sw', expect='English Garden')

		# English Garden

		rain = ''
		while 'dreary' not in rain:
			rain = self.do('x rain')

		self.do('stand in rain', expect='walrus')
		self.do('get walrus', expect='Taken')
		self.do('wear walrus', expect='earlobes')

		self.do('get out of rain')
		self.do('n', expect='Topiary of Time')
		self.do('n', expect='Fountain Court')
		self.do('nw', expect='Greenhouse')
		self.do('nw', expect='Hothouse')

		# Hothouse

		self.do('get salamander with coaster', expect='You now have')

		self.do('se', expect='Greenhouse')
		self.do('w', expect='Back of Museum')
		self.do('n', expect='Desolate Field')
		self.do('ne', expect='River Bed')
		self.do('n', expect='UpRiver')

		# UpRiver

		self.do('put ring in pool')
	
def main():
	implementation = Implementation()
	playthrough = Playthrough(implementation)
	playthrough.run()
	implementation.close()

if __name__=='__main__':
	main()

