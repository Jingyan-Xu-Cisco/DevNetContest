<?php
$dbms='mysql';
$host='10.80.9.1'; //数据库主机名
$dbName='TLPR_test';    //使用的数据库
$user='remote';      //数据库连接用户名
$pass='C1sc0123';          //对应的密码
$dsn="$dbms:host=$host;dbname=$dbName";
$i = 1;
$left = 1;
$center=2;
$right=3;
$I_want = $right;

try {
    $dbh = new PDO($dsn, $user, $pass);
//    echo "连接成功<br/>";

    foreach ($dbh->query('SELECT distinct time from CDP_table order by time desc limit 3') as $row) {
        if ($i == $I_want ) { echo $row[0] . "<br>" ;}
        $i = $i + 1;
    }
    $dbh = null;
} catch (PDOException $e) {
    die ("Error!: " . $e->getMessage() . "<br/>");
}
?>
