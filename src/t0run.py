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

def main():
	implementation = Implementation()
	playthrough = Playthrough(implementation)
	playthrough.run()
	implementation.close()

if __name__=='__main__':
	main()

