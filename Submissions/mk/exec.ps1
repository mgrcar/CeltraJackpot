$i = $args[0]
$e = $args[1]
echo "java -cp Jackpot\src gambler http://localhost/CeltraJackpot/mk.$i.$e/$e"
java -cp Jackpot\src gambler http://localhost/CeltraJackpot/mk.$i.$e/$e