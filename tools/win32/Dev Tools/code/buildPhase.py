import os
import subprocess
import sys


os.chdir('../../../resources')
cmd = ''
for phasenum in ['3', '3.5', '4', '5', '5.5', '6', '7', '8', '9', '10', '11', '12', '13']:
	print 'phase_%s' % (phasenum)
	cmd = 'multify -cf phase_%s.mf phase_%s' % (phasenum, phasenum)
	p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
	v = p.wait()
	if v != 0:
		print 'The following command returned non-zero value (%d): %s' % (v, cmd[:100] + '...')
		sys.exit(1)
for stagenum in ['3', '4']:
	print 'stage_%s' % (stagenum)
	cmd = 'multify -cf stage_%s.mf stage_%s' % (stagenum, stagenum)
	p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
	v = p.wait()
	if v != 0:
		print 'The following command returned non-zero value (%d): %s' % (v, cmd[:100] + '...')
		sys.exit(1)		
