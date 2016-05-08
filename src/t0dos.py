import subprocess
import os
import sys
import tempfile
import glob
import select
import time
import signal

# Number of seconds to wait for the game to start up.
SLEEP_WAIT = 14

class Emulator(object):
	def __init__(self, contents_dir):
		self._contents_dir = contents_dir
		self._emu = None
		self._rlist = [sys.stdin]

	def launch(self):

		self._emu = subprocess.Popen(
			args = [
				'dosemu',
				'-f'+os.path.join(self._contents_dir, 'c', 'dosemu.conf'),
				'-quiet',
				'-dumb',
				'--Fimagedir',
				self._contents_dir,
				'T-ZERO',
				],
			stdin = subprocess.PIPE)

		time.sleep(1)

		for startup_command in [
				'T-ZERO',
				'',
				'SCRIPT',
			]:

			self._emu.stdin.write(startup_command+'\r\n')

			if startup_command=='T-ZERO':
				print
				print 'Now sleeping for', SLEEP_WAIT, 'seconds while the game starts up.'
				print
				time.sleep(SLEEP_WAIT)
				print 'Sleep finished.'
			else:
				time.sleep(1)

	def run(self):
		while True:

			ready = select.select(
				self._rlist,
				[], # wlist
				[], # xlist
			)

			if sys.stdin in ready[0]:
				input = sys.stdin.readline()

				if input.endswith('\n'):
					input = input[:-1]+'\r\n'

				self._emu.stdin.write(input)

	def close(self):
		print 'Closing emulator.'
		self._emu.kill()

def copy_in_original(source, target):

	# The target given is a directory for drives.
	# Everything we're doing is on drive C,
	# so just create that.
	target = os.path.join(target, 'c')
	os.mkdir(target)

	for filename in [
		'HINT.DAT',
		'T-0.DAT',
		'T-ZERO.DAT',
		'T-ZERO.EXE',
		'dosemu.conf',
		]:

		source_filename = os.path.join(source, filename)
		target_filename = os.path.join(target, filename)

		contents = open(source_filename).read()
		open(target_filename, 'wb').write(contents)

def main():

	temp_dir = tempfile.mkdtemp(prefix='temp_t0dos')

	# FIXME: original directory should be configurable
	copy_in_original(source='orig', target=temp_dir)

	emu = Emulator(contents_dir=temp_dir)

	def sigterm_handler(signum, frame):
		print '--- SIGTERM received ---'
		print 'Emu is ',emu
		emu.close()
		sys.exit()

	signal.signal(signal.SIGTERM, sigterm_handler)

	emu.launch()
	emu.run()

if __name__=='__main__':
	main()
