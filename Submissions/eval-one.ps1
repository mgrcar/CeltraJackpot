$c = $args[0]
cd $c

for ($i = 1; $i -le 100; $i++) {
	for ($e = 1; $e -le 10; $e++) {
		if (!(Test-Path "..\Results\$c.$i.$e.done")) {
			Remove-Item "..\Results\$c.$i.$e.*"
			.\exec.ps1 $i $e
		}
	}
}