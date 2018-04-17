<?php
include("functions_external.php"); // more includes
$entry = ""; // more variables
function sqli($data)
  $data = sqli_check_1($data); ... return $data;
?>
<html>...<header><h1>bWAPP</h1> <h2>an extremely buggy web app !</h2> </header>
<div id="menu">  ... </div> // other divs
<div id="main">
  <h1>SQL Injection - Stored (Blog)</h1>
  <form action="<?php echo($_SERVER["SCRIPT_NAME"]);?>" method="POST">
      <?php
        $entry = sqli($_POST["entry"]);
        $owner = $_SESSION["login"];
        $sql = "INSERT INTO blog (date, entry, owner) VALUES (now(),'" . $entry . "','" . $owner . "')";
        $recordset = $link->query($sql);
      ?>
  </form>
  <?php
    $sql = "SELECT * FROM blog";
    $recordset = $link->query($sql);
    while($row = $recordset->fetch_object())
       <tr height="40">
            <td align="center"> <?php echo $row->id; ?></td>
            <td><?php echo $row->owner; ?></td>
            <td><?php echo $row->date; ?></td>
            <td><?php echo xss_check_3($row->entry); ?></td>
        </tr>
  ?>
</div>
<div id="side">...</div> // other divs
</body></html>
