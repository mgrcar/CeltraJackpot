$i = $args[0]
$e = $args[1]
echo "Invoke-WebRequest http://localhost/Play/localhost_celtrajackpot_tj.$i.$e/$e"
do {
	$r = Invoke-WebRequest http://localhost/Play/localhost_celtrajackpot_tj.$i.$e/$e
	Start-Sleep -s 1
} while ($r.Content -eq "Already running")
