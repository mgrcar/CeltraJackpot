cd $args[0]

for ($i = 1; $i -le 100; $i++) {
	for ($e = 1; $e -le 10; $e++) {
		.\exec.ps1 $i $e
	}
}