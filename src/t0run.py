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
		self._monitors = []

	def addMonitor(self, monitor):
		self._monitors.append(monitor)
		monitor.setImplementation(self)

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

	def _pushToMonitors(self, command, response):
		for monitor in self._monitors:
		    monitor.handle(command, response)

	def run(self):
		print 'Beginning run.'

		startupText = self.read()
		print startupText
		self._pushToMonitors('', startupText)

	def do(self,
		command,
		expect=None):
		
		self.write(command)
		response = self.read()

		if expect is not None and not expect in response:
			self.close()
			raise Exception('"%s" was not found in:\n=== %s\n%s' % (
				expect,
				command,
				response))

		self._pushToMonitors(command, response)
		return response

	def close(self):
		print 'Terminating process', self._sub.pid, 'here'
		self._sub.terminate()
		print 'Waiting...'
		self._sub.wait()

		for monitor in self._monitors:
		    monitor.close()

class Monitor(object):
	"""
	A Monitor watches the game being played
	and interferes where it wants.
	"""
	def __init__(self):
		self._implementation = None

	def setImplementation(self, implementation):
		self._implementation = implementation

	def handle(self, command, response):
		raise Exception("Abstract method called")

	def close(self):
		pass


class Playthrough(Monitor):
	"""
	Playthrough watches for the beginning of the game,
	then injects the commands to play the
	whole game through.
	"""

	def handle(self, command, reponse):
		if command=='':
		    # at the beginning of the run;
		    # start the playthrough
		    self.run()

	def run(self):
		impl = self._implementation

		impl.do('inventory', expect = 'in your possession')
		impl.do('x slip', expect='walking papers')
		impl.do('read slip', expect='too near completion')
		impl.do('x compass', expect='cardinal directions')
		impl.do('x me', expect='fade into the woodwork')
		impl.do('x journal page', expect='cryptic')
		impl.do('x fatigues', expect='commodious')
		impl.do('x fob pocket', expect='just the right')
		impl.do('x thigh pocket', expect='mind of its own')

		# Field of Poppies

		impl.do('nw', expect='Field of Poppies')
		impl.do('x poppy', expect='dry husk')
		impl.do('get seed', expect='bursts')

		# Field of Stone

		impl.do('s', expect='Field of Stone')
		birdpoo = ''
		birdpoo += impl.do('leave no stone unturned', expect='prehistoric')
		birdpoo += impl.do('get claw', expect='Taken')
		birdpoo += impl.do('x tern', expect='tirelessly')

		while 'taking aim' not in birdpoo:
			birdpoo += impl.do('wait')

		impl.do('stone terns', expect='stoned')
		impl.do('get tern', expect='turn to stone')
		impl.do('get feather', expect='Taken')

		# off to the Coldhouse

		impl.do('se', expect='Desolate Field')
		impl.do('s', expect='Back of Museum')
		impl.do('e', expect='Greenhouse')
		impl.do('ne', expect='Coldhouse')

		# Coldhouse

		impl.do('pull lever', expect='arctic')
		impl.do('get token', expect='Taken')
		impl.do('get lever', expect='Taken')

		impl.do('sw', expect='Greenhouse')
		impl.do('e', expect='Shed')

		# Shed

		impl.do('x shelf', expect='splintery')
		impl.do('get extractor', expect='Taken')
		impl.do('get fixer-upper', expect='Taken')

		impl.do('w', expect='Greenhouse')
		impl.do('open door', expect='Opened')
		impl.do('n', expect='Caretaker\'s Cottage')

		# Cottage

		impl.do('get bell', expect='Taken')

		impl.do('e', expect='Pantry')

		# Pantry

		impl.do('get jar', expect='Taken')

		impl.do('w', expect='Caretaker\'s Cottage')
		impl.do('s', expect='Greenhouse')
		impl.do('se', expect='Fountain Court')
		impl.do('s', expect='Topiary')
		impl.do('e', expect='Topiary')

		# Topiary

		topiary_path = 'EESSENNNESWSESSWWWWNNESWSEEEEN'

		for move in topiary_path:
			result = impl.do(move, 'to the Northwest')

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
						impl.do('pull '+monster+' with '+tool,
							expect='which now reads')

		impl.do('e', expect='Amazing Space')

		# Amazing Space

		impl.do('attach fixer-upper to extractor', expect='lightning')
		impl.do('get latchkey', expect='Taken')
		impl.do('get orange', expect='Taken')

		impl.do('e', expect='Platform Over River')
		impl.do('ne', expect='Suspension Bridge')
		impl.do('snap suspenders', expect='retort')
		impl.do('ne', expect='Across the River')
		impl.do('e', expect='Junkyard')

		# Junkyard

		impl.do('call rag man Anagram', expect='proper name')
		impl.do('ask Anagram about violets', expect='wallflower')
		impl.do('dig in dump with claw', expect='debugged')
		impl.do('get ring', expect='swoops')
		impl.do('get code', expect='Taken')
		impl.do('get flag', expect='Taken')
		impl.do('give code to anagram', expect='wire-frame')

		impl.do('w', expect='Across the River')
		impl.do('sw', expect='Suspension Bridge')

		impl.do('snap suspenders', expect='retort')
		impl.do('tie loop to stanchion', expect='infinite')
		impl.do('snap suspenders', expect='retort')
		impl.do('d', expect='On the Rocks')

		# On the Rocks

		impl.do('get coaster', expect='Taken')

		impl.do('u', expect='Suspension Bridge')
		impl.do('snap suspenders', expect='retort')
		impl.do('sw', expect='Platform Over River')
		impl.do('sw', expect='English Garden')

		# English Garden

		rain = ''
		while 'dreary' not in rain:
			rain = impl.do('x rain')

		walrus = ''
		while 'walrus' not in walrus:
			walrus += impl.do('stand in rain')

		impl.do('get walrus', expect='Taken')
		impl.do('wear walrus', expect='earlobes')

		impl.do('get out of rain')
		impl.do('n', expect='Topiary of Time')
		impl.do('n', expect='Fountain Court')
		impl.do('nw', expect='Greenhouse')
		impl.do('nw', expect='Hothouse')

		# Hothouse

		impl.do('get salamander with coaster', expect='You now have')

		impl.do('se', expect='Greenhouse')
		impl.do('w', expect='Back of Museum')
		impl.do('sw', expect='West Side of Museum')
		impl.do('s', expect='Cornerstone')
		impl.do('se', expect='Museum Stairs')
		impl.do('n', expect='Portico of Museum')
		impl.do('unlock door with latchkey', expect='Unlocked')
		impl.do('open door', expect='Opened')

		# Museum

		impl.do('n', expect='Foyer')
		impl.do('n', expect='West-East')
		impl.do('open door', expect='Opened')
		impl.do('n', expect='Administrative')
		impl.do('get slow mirror', expect='Taken')
		impl.do('s', expect='West-East')

		impl.do('w', expect='Hall of Clocks')
		impl.do('n', expect='Counter-Clockwise')
		impl.do('jump counterclockwise', expect='Spiral Staircase')

		impl.do('open door', expect='Opened')
		impl.do('e', expect='Library')
		impl.do('read plaque', expect='curl')
		impl.do('press button')

		return
		#### --- add in later

		impl.do('e', expect='Turn in Hall')
		impl.do('s', expect='South-North Hall')
		impl.do('open door', expect='Opened')
		impl.do('e', expect='Computer Room')
		impl.do('n', expect='Green Room')

		# Green Room

		impl.do('open door', expect='lethal')
		impl.do('open jar', expect='pressure')
		impl.do('close jar', expect='Closed')

		impl.do('n', expect='Countdown')
		impl.do('unlock north door with latchkey')
		impl.do('open north door')

class Logger(Monitor):

	def __init__(self,
		to_stdout = True,
		to_filename = None):

		super(Logger, self).__init__()

		self._to_stdout = to_stdout

		if to_filename is not None:
			self._logfile = open(to_filename, 'w')
		else:
		    	self._logfile = None

	def handle(self, command, response):

		content = '==== %s\n%s\n' % (
			command,
			response)

		if self._to_stdout:
			print content

		if self._logfile is not None:
		    self._logfile.write(content)

	def close(self):
		if self._logfile is not None:
		    self._logfile.close()

MOVEMENTS = (
	'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw',
	'up', 'down',
	'jump counterclockwise',
	'jump clockwise',
	)

class RoomNoticer(Monitor):

	def __init__(self):
		super(RoomNoticer, self).__init__()

		self._seenRooms = set()

	def handle(self, command, response):

		if not command.lower() in MOVEMENTS:
		    return

		response = response.split('\n')

		# Either the room name is at the end
		# of the text, with blank lines around it
		# (in the case that we didn't just move)
		# or it's on the first nonblank line
		# (in the case that we did).

		roomName = response[response.index('')+1]

		self._enterRoom(name=roomName,
			firstTime = not roomName in self._seenRooms)

		self._seenRooms.add(roomName)

	def _enterRoom(self, name, firstTime):
	    print 'Room name is [%s]. First? %d.' % (name, firstTime)

def main():
	implementation = Implementation()
	implementation.addMonitor(Playthrough())
	implementation.addMonitor(Logger(
		to_stdout = True,
		to_filename = 't0run.log',
		))
	implementation.run()
	implementation.close()

if __name__=='__main__':
	main()

