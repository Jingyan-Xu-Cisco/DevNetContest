<html>
<h1>Hello! This program is to generate current topology</h1><br>
<?php

$command = escapeshellcmd('/home/layim/code/genTopology.sh');
$output = shell_exec($command);
header('Location: http://10.80.9.2/app/TLPR/topology.php');

?>
</html>
